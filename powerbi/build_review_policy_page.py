"""Build the comparison page in a local Power BI Project copy."""

import argparse
import json
from pathlib import Path
import shutil
from tempfile import mkdtemp
from uuid import uuid4


PAGE_NAME = "Review Policy Comparison"
TRIAGE_NAME = "Fraud Triage"
VISUAL_SCHEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/"
    "definition/visualContainer/2.7.0/schema.json"
)
RANKS = "September_Ranks"
NAVY = "#0F172A"
SLATE = "#1E3A5F"
TEAL = "#0F766E"
SECONDARY = "#475569"
BORDER = "#CBD5E1"
MUTED = "#EEF2F7"
CANVAS = "#0C1422"
PANEL = "#131E30"
INSET = "#0E1828"
DIVIDER = "#2B3B51"
INK = "#F0F5FA"
SUBTLE = "#AABACD"
MINT = "#62DDBD"
BLUE = "#9EB8E4"
TITLE_FONT = "Bricolage Grotesque"
NUMBER_FONT = "IBM Plex Mono"
LOGO_NAME = "bfi-fraud-triage-mark.png"
LOGO_SOURCE = Path(__file__).resolve().parents[1] / "assets" / "fraud-triage-preview-mark.png"
SLICERS = {"bfiCohort", "bfiCapacity", "bfiPeriod"}
LIGHT_VISUALS = {"bfiHeader", "bfiSimulated", "bfiMethodology", *SLICERS,
                 "bfiDailyYield", "bfiScenarioLift", "bfiScorecard"}
TRIAGE_VISUALS = (LIGHT_VISUALS - {"bfiSimulated", "bfiMethodology"}) | {"bfiLogo", "bfiBrand"}
CARD_SPECS = (
    ("Amount Baseline Fraud-labelled Selected", "Amount baseline", SLATE, 24),
    ("Logistic Regression Fraud-labelled Selected", "Logistic regression", TEAL, 440),
    ("Model Difference", "Model difference", NAVY, 856),
)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, content):
    path.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def literal(value):
    return {"expr": {"Literal": {"Value": value}}}


def colour(value):
    return {"solid": {"color": literal(f"'{value}'")}}


def signed_colour():
    difference = field(RANKS, "Model Difference", "Measure")
    return {"solid": {"color": {"expr": {"Conditional": {
        "Cases": [
            {"Condition": {"Comparison": {"ComparisonKind": op, "Left": difference,
                                          "Right": {"Literal": {"Value": "0D"}}}},
             "Value": {"Literal": {"Value": f"'{color}'"}}}
            for op, color in ((1, MINT), (3, BLUE))
        ],
        "DefaultValue": {"Literal": {"Value": f"'{INK}'"}},
    }}}}}


def formatting(**properties):
    return [{"properties": properties}]


def field(entity, name, kind="Column", alias=None):
    source = {"Source": alias} if alias else {"Entity": entity}
    return {kind: {"Expression": {"SourceRef": source}, "Property": name}}


def projection(entity, name, label, kind="Column", *, aggregate=False):
    expression = field(entity, name, kind)
    query_ref = f"{entity}.{name}"
    if aggregate:
        expression = {"Aggregation": {"Expression": expression, "Function": 0}}
        query_ref = f"Sum({query_ref})"
    return {"field": expression, "queryRef": query_ref, "nativeQueryRef": label, "displayName": label}


def measure(name, label):
    return projection(RANKS, name, label, "Measure")


def position(x, y, width, height, order):
    return {"x": x, "y": y, "width": width, "height": height, "z": order, "tabOrder": order}


def container(title=None, subtitle=None, *, dark=False, fill=None):
    result = {
        "background": formatting(show=literal("true"), color=colour(fill or (PANEL if dark else "#FFFFFF")),
                                 transparency=literal("0D")),
        "border": formatting(show=literal("true"), color=colour(DIVIDER if dark else BORDER), radius=literal("8D")),
    }
    if title:
        result["title"] = formatting(
            show=literal("true"), text=literal(f"'{title}'"), fontColor=colour(INK if dark else NAVY),
            fontFamily=literal(f"'{TITLE_FONT if dark else 'Segoe UI Semibold'}'"), fontSize=literal("12D"),
        )
        result["subTitle"] = formatting(show=literal("false"))
    if subtitle:
        result["subTitle"] = formatting(
            show=literal("true"), text=literal(f"'{subtitle}'"),
            fontColor=colour(SUBTLE if dark else SECONDARY), fontSize=literal("10D"),
        )
    return result


def visual(key, kind, bounds, *, roles=None, objects=None, style=None):
    body = {"visualType": kind}
    if roles:
        body["query"] = {"queryState": {role: {"projections": p} for role, p in roles.items()}}
    if objects:
        body["objects"] = objects
    if style:
        body["visualContainerObjects"] = style
    return {"$schema": VISUAL_SCHEMA, "name": key, "position": position(*bounds), "visual": body}


def text_box(key, bounds, *lines, dark=False):
    paragraphs = [
        {"textRuns": [{"value": label, "textStyle": {
            "fontFamily": TITLE_FONT if dark else ("Segoe UI Semibold" if bold else "Segoe UI"),
            "fontSize": f"{size}pt", "color": color,
            **({"fontWeight": "bold"} if dark and bold else {}),
        }}]}
        for label, size, color, bold in lines
    ]
    return visual(key, "textbox", bounds, objects={"general": formatting(paragraphs=paragraphs)})


def filter_for(entity, condition):
    return {"Version": 2, "From": [{"Name": "f", "Entity": entity, "Type": 0}],
            "Where": [{"Condition": condition}]}


def choice_slicer(key, title, entity, name, default, bounds):
    selected = filter_for(entity, {"In": {
        "Expressions": [field(entity, name, alias="f")],
        "Values": [[{"Literal": {"Value": default}}]],
    }})
    return visual(key, "advancedSlicerVisual", bounds,
                  roles={"Values": [projection(entity, name, title)]},
                  objects={
                      "layout": formatting(rowCount=literal("1L"), columnCount=literal("2L")),
                      "selection": formatting(singleSelect=literal("true"), strictSingleSelect=literal("true")),
                      "general": formatting(filter={"filter": selected}),
                  }, style=container(title))


def matching_cards(visual_files):
    cards = {}
    for path in visual_files:
        content = read_json(path)
        body = content.get("visual", {})
        role = {"cardVisual": "Data", "card": "Values"}.get(body.get("visualType"))
        if role is None:
            continue
        projections = body.get("query", {}).get("queryState", {}).get(role, {}).get("projections", [])
        if len(projections) != 1:
            continue
        binding = projections[0].get("field", {}).get("Measure", {})
        entity = binding.get("Expression", {}).get("SourceRef", {}).get("Entity")
        name = binding.get("Property")
        if entity == RANKS and name in {spec[0] for spec in CARD_SPECS}:
            if name in cards:
                raise ValueError(f"More than one card uses {name}.")
            cards[name] = path
    if len(cards) != 3:
        raise ValueError("Could not identify the three verified KPI cards.")
    return cards


def format_cards(cards, *, dark=False):
    updates = {}
    for order, (name, label, color, x) in enumerate(CARD_SPECS, start=10):
        content = read_json(cards[name])
        body = content["visual"]
        kind = body.get("visualType")
        if kind not in ("cardVisual", "card"):
            raise ValueError(f"{name} is bound to an unexpected visual type: {kind}.")
        role = "Data" if kind == "cardVisual" else "Values"
        binding = body["query"]["queryState"][role]["projections"][0]
        binding["nativeQueryRef"] = label
        binding["displayName"] = label
        fill = None
        if dark:
            x, width, order = {
                "Model difference": (24, 528, 10),
                "Amount baseline": (568, 336, 11),
                "Logistic regression": (920, 336, 12),
            }[label]
            content["position"] = position(x, 222, width, 108, order)
            fill = "#152C3A" if label == "Model difference" else PANEL
            value_colour = signed_colour() if label == "Model difference" else colour(
                BLUE if label == "Amount baseline" else MINT
            )
            label_text = ("Model minus baseline" if label == "Model difference" else label)
            label_font = {"fontFamily": literal(f"'{TITLE_FONT}'")}
            label_size = "12D"
            number_font = {"fontFamily": literal(f"'{NUMBER_FONT}'"), "labelDisplayUnits": literal("1D")}
            value_size = "33D" if label == "Model difference" else "28D"
            binding["nativeQueryRef"] = label_text
            binding["displayName"] = label_text
        else:
            content["position"] = position(x, 176, 400, 96, order)
            value_colour, label_font, label_size, number_font, value_size = colour(color), {}, "11D", {}, "28D"
        body.setdefault("visualContainerObjects", {}).update(container(dark=dark, fill=fill))
        objects = body.setdefault("objects", {})
        if kind == "cardVisual":
            objects["fillCustom"] = formatting(show=literal("false"))
            objects["value"] = formatting(fontSize=literal(value_size), fontColor=value_colour, **number_font)
            objects["label"] = formatting(show=literal("true"), fontSize=literal(label_size), **label_font,
                                          **({"fontColor": colour(SUBTLE)} if dark else {}))
            if dark:
                for key in ("fillCustom", "value", "label"):
                    objects[key][0]["selector"] = {"id": "default"}
        else:
            objects["labels"] = formatting(fontSize=literal(value_size), color=value_colour, **number_font)
            objects["categoryLabels"] = formatting(show=literal("true"), fontSize=literal(label_size), **label_font,
                                                    **({"color": colour(SUBTLE)} if dark else {}))
        updates[cards[name]] = content
    return updates


def supporting_visuals():
    baseline = measure(CARD_SPECS[0][0], CARD_SPECS[0][1])
    model = measure(CARD_SPECS[1][0], CARD_SPECS[1][1])
    date = projection("DimDate", "Date", "Date")
    line = visual("bfiDailyYield", "lineChart", (24, 288, 816, 208, 20),
                  roles={"Category": [date], "Y": [baseline, model]},
                  objects={
                      "legend": formatting(show=literal("true"), showTitle=literal("false")),
                      "lineStyles": [
                          {"properties": {"showMarker": literal("true"), "markerSize": literal("4D")}},
                          {"properties": {"lineStyle": literal("'dashed'")},
                           "selector": {"metadata": model["queryRef"]}},
                      ],
                      "dataPoint": [
                          {"properties": {"fill": colour(color)}, "selector": {"metadata": metric["queryRef"]}}
                          for metric, color in ((baseline, SLATE), (model, TEAL))
                      ],
                  }, style=container("Daily queue yield"))
    line["visual"]["query"]["sortDefinition"] = {
        "sort": [{"field": date["field"], "direction": "Ascending"}], "isDefaultSort": False,
    }
    scenario = "September_Scenario_Lift"
    table_style = {
        "grid": formatting(rowPadding=literal("4D"), gridVertical=literal("false"),
                           gridHorizontal=literal("true"), gridHorizontalColor=colour(MUTED)),
        "columnHeaders": formatting(fontSize=literal("10D"), backColor=colour(MUTED),
                                    fontColor=colour(NAVY), bold=literal("true"),
                                    autoSizeColumnWidth=literal("true"),
                                    columnAdjustment=literal("'growToFit'")),
        "values": formatting(fontSize=literal("11D"), fontColorPrimary=colour(NAVY),
                             fontColorSecondary=colour(NAVY), backColorPrimary=colour("#FFFFFF"),
                             backColorSecondary=colour("#F8FAFC")),
    }
    matrix = visual("bfiScenarioLift", "pivotTable", (856, 288, 400, 208, 21),
                    roles={
                        "Rows": [projection(scenario, "Cohort", "Eligible cohort")],
                        "Columns": [projection(scenario, "DailyCapacity", "Reviews/day")],
                        "Values": [projection(scenario, "ModelDifference", "Model difference", aggregate=True)],
                    }, objects={**table_style,
                                "rowHeaders": formatting(fontSize=literal("11D"), fontColor=colour(NAVY)),
                                "subTotals": formatting(rowSubtotals=literal("false"), columnSubtotals=literal("false")),
                                "grandTotals": formatting(rowGrandTotals=literal("false"), columnGrandTotals=literal("false"))},
                    style=container("Full-September reference", "Additional fraud labels selected by the model"))
    scorecard = visual(
        "bfiScorecard", "tableEx", (24, 512, 1232, 160, 22),
        roles={"Values": [
            projection("Review Policy", "Policy", "Policy"),
            measure("Reviews Selected", "Reviews"),
            measure("Fraud-labelled Selected", "Fraud-labelled selected"),
            measure("Legitimate Reviews", "Legitimate reviews"),
            measure("Queue Precision", "Queue precision"),
            measure("Cohort Recall", "Cohort recall"),
            measure("Fraud-labelled Value Selected", "Fraud-labelled value selected"),
        ]},
        objects={**table_style, "total": formatting(totals=literal("false"))},
        style=container("Policy scorecard"),
    )
    return [
        text_box("bfiHeader", (24, 16, 840, 64, 1),
                 (PAGE_NAME, 26, NAVY, True),
                 ("Fraud-labelled transactions selected at equal daily review limits", 11, SECONDARY, False)),
        text_box("bfiSimulated", (1032, 24, 224, 32, 2), ("Simulated data", 11, TEAL, True)),
        choice_slicer("bfiCohort", "Eligible cohort", "Review Cohort", "Cohort",
                      "'All transactions'", (24, 80, 400, 88, 3)),
        choice_slicer("bfiCapacity", "Reviews per day", "Review Capacity", "DailyCapacity",
                      "50L", (440, 80, 296, 88, 4)),
        visual("bfiPeriod", "slicer", (752, 80, 504, 88, 5), roles={"Values": [date]},
               objects={"data": formatting(mode=literal("'Between'")),
                        "header": formatting(show=literal("false"))}, style=container("September 2018")),
        line, matrix, scorecard,
        text_box("bfiMethodology", (24, 680, 1232, 24, 23),
                 ("Simulated holdout. Labels are retrospective. Selected value sums the amounts of selected fraud-labelled transactions.",
                  9, SECONDARY, False)),
    ]


def triage_visuals():
    light = {item["name"]: item for item in supporting_visuals()}
    controls = []
    for key, title, x, width in (
        ("bfiCohort", "Eligible transactions", 24, 456),
        ("bfiCapacity", "Reviews per day", 496, 288),
        ("bfiPeriod", "September 2018 date range", 800, 456),
    ):
        item = light[key]
        item["position"] = position(x, 120, width, 86, item["position"]["tabOrder"])
        body = item["visual"]
        body["visualContainerObjects"] = container(title, dark=True, fill=INSET)
        objects = body["objects"]
        if key == "bfiPeriod":
            objects["numericInputStyle"] = formatting(
                background=colour(PANEL), fontColor=colour(INK), fontFamily=literal(f"'{TITLE_FONT}'"),
            )
            objects["slider"] = formatting(color=colour(MINT), handleBorderColor=colour(MINT))
        else:
            objects["background"] = [
                {"properties": {"show": literal("true"), "color": colour(fill)},
                 "selector": {"id": state}}
                for state, fill in (("default", PANEL), ("selected", "#183D3D"))
            ]
            objects["value"] = [
                {"properties": {"fontColor": colour(text), "fontFamily": literal(f"'{TITLE_FONT}'"),
                                "fontSize": literal("11D")},
                 "selector": {"id": state}}
                for state, text in (("default", INK), ("selected", MINT))
            ]
        controls.append(item)

    date = projection("DimDate", "Date", "Date")
    difference = measure("Model Difference", "Model minus baseline")
    baseline = measure(CARD_SPECS[0][0], CARD_SPECS[0][1])
    model = measure(CARD_SPECS[1][0], CARD_SPECS[1][1])
    axis = {"labelColor": colour(SUBTLE), "fontFamily": literal(f"'{NUMBER_FONT}'"),
            "fontSize": literal("10D"), "showAxisTitle": literal("false")}
    chart = visual(
        "bfiDailyYield", "clusteredColumnChart", (24, 346, 832, 206, 20),
        roles={"Category": [date], "Y": [difference], "Tooltips": [baseline, model]},
        objects={
            "legend": formatting(show=literal("false")),
            "categoryAxis": formatting(**axis),
            "valueAxis": formatting(**axis, gridlineShow=literal("true"), gridlineColor=colour(DIVIDER)),
            "dataPoint": [
                {"properties": {"defaultColor": colour(MINT)}},
                {"properties": {"fill": signed_colour()},
                 "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}},
            ],
            "y1AxisReferenceLine": formatting(show=literal("true"), value=literal("0D"),
                                             lineColor=colour(SUBTLE), style=literal("'solid'"),
                                             width=literal("1D")),
        },
        style={
            **container("Where the model gained or lost", "Fraud-labelled selections · mint model ahead · blue baseline ahead",
                        dark=True),
            "visualTooltip": formatting(show=literal("true")),
        },
    )
    chart["visual"]["query"]["sortDefinition"] = {
        "sort": [{"field": date["field"], "direction": "Ascending"}], "isDefaultSort": False,
    }

    matrix, scorecard = light["bfiScenarioLift"], light["bfiScorecard"]
    matrix["position"] = position(872, 346, 384, 206, 21)
    matrix["visual"]["visualContainerObjects"] = container(
        "Does capacity change the result?", "Full-September difference · model minus baseline", dark=True, fill=INSET,
    )
    matrix["visual"]["objects"]["rowHeaders"] = formatting(
        fontSize=literal("11D"), fontFamily=literal(f"'{TITLE_FONT}'"),
        fontColor=colour(INK), backColor=colour(INSET),
    )
    scorecard["position"] = position(24, 568, 1232, 128, 22)
    scorecard["visual"]["visualContainerObjects"] = {
        **container("Review trade-offs", dark=True),
        "visualHeader": formatting(show=literal("true"), showTooltipButton=literal("true"),
                                   foreground=colour(INK), background=colour(PANEL)),
        "visualHeaderTooltip": formatting(
            type=literal("'Default'"),
            text=literal("'Simulated Fraud Detection Handbook transactions. Fraud labels are used retrospectively; "
                         "the source has no confirmation timestamps. Precision is the labelled share of reviews. "
                         "Recall is the share of eligible fraud labels selected. Fraud-labelled value sums the "
                         "transaction amounts of selected rows with a fraud label.'"),
        ),
    }
    for item in (matrix, scorecard):
        objects = item["visual"]["objects"]
        objects["grid"] = formatting(rowPadding=literal("4D"), gridVertical=literal("false"),
                                     gridHorizontal=literal("true"), gridHorizontalColor=colour(DIVIDER))
        objects["columnHeaders"] = formatting(
            fontSize=literal("10D"), fontFamily=literal(f"'{TITLE_FONT}'"), backColor=colour(INSET),
            fontColor=colour(SUBTLE), bold=literal("true"), autoSizeColumnWidth=literal("true"),
        )
        objects["values"] = formatting(
            fontSize=literal("11D"), fontFamily=literal(f"'{NUMBER_FONT}'"),
            fontColorPrimary=colour(INK), fontColorSecondary=colour(INK),
            backColorPrimary=colour(PANEL), backColorSecondary=colour(INSET),
        )
    for entry, label in zip(scorecard["visual"]["query"]["queryState"]["Values"]["projections"],
                            ("Policy", "Reviews", "Fraud-labelled", "Legitimate", "Precision", "Recall",
                             "Fraud-labelled value"), strict=True):
        entry.update(nativeQueryRef=label, displayName=label)

    image_ref = {"expr": {"ResourcePackageItem": {
        "PackageName": "RegisteredResources", "PackageType": 1, "ItemName": LOGO_NAME,
    }}}
    return [
        visual("bfiLogo", "image", (24, 12, 36, 36, 0),
               objects={"general": formatting(imageUrl=image_ref)},
               style={"background": formatting(show=literal("false")),
                      "border": formatting(show=literal("false")),
                      "visualHeader": formatting(show=literal("false"))}),
        text_box("bfiBrand", (70, 17, 540, 29, 1), ("Banking Fraud Intelligence", 14, INK, True), dark=True),
        text_box("bfiHeader", (24, 52, 1220, 65, 2),
                 (TRIAGE_NAME, 29, INK, True),
                 ("Prioritising transactions under a fixed daily review limit.", 12, SUBTLE, False), dark=True),
        *controls, chart, matrix, scorecard,
    ]


def build_page(page_path, staged_path, *, dark=False):
    page = read_json(page_path / "page.json")
    new_visuals = triage_visuals() if dark else supporting_visuals()
    visual_files = sorted(page_path.glob("visuals/*/visual.json"))
    managed = {item["name"] for item in new_visuals}
    recognised = LIGHT_VISUALS | TRIAGE_VISUALS if dark else LIGHT_VISUALS
    existing = {path.parent.name: path for path in visual_files if path.parent.name in recognised}
    valid_layouts = (LIGHT_VISUALS, TRIAGE_VISUALS) if dark else (LIGHT_VISUALS,)
    if existing and existing.keys() not in valid_layouts:
        raise ValueError("Expected a complete comparison layout generated by this builder.")
    cards = matching_cards([path for path in visual_files if path not in existing.values()])
    updates = format_cards(cards, dark=dark)
    if len(visual_files) != len(cards) + len(existing):
        raise ValueError("Expected the original three-card page or the complete page generated by this builder.")
    for item in new_visuals:
        path = existing.get(item["name"])
        if path is None:
            continue
        original = read_json(path)
        body = original["visual"]
        updated = item["visual"]
        if original["name"] != item["name"]:
            raise ValueError(f"Unexpected visual in {path.parent.name}.")
        if dark and item["name"] not in SLICERS:
            old_chart = item["name"] == "bfiDailyYield" and body["visualType"] == "lineChart"
            if body["visualType"] != updated["visualType"] and not old_chart:
                raise ValueError(f"Unexpected visual type in {path.parent.name}.")
            updates[path] = item
            continue
        if body["visualType"] != updated["visualType"]:
            raise ValueError(f"Unexpected visual in {path.parent.name}.")
        original["position"] = item["position"]
        body.setdefault("visualContainerObjects", {}).update(updated.get("visualContainerObjects", {}))
        projections_by_ref = {
            entry["queryRef"]: entry
            for role in updated.get("query", {}).get("queryState", {}).values()
            for entry in role["projections"]
        }
        for role in body.get("query", {}).get("queryState", {}).values():
            for entry in role.get("projections", []):
                new_projection = projections_by_ref.get(entry["queryRef"])
                if new_projection:
                    entry["displayName"] = new_projection["displayName"]
                    entry["nativeQueryRef"] = new_projection["nativeQueryRef"]
        new_objects = updated.get("objects", {}).copy()
        if item["name"] in SLICERS:
            new_objects.pop("general", None)
        body.setdefault("objects", {}).update(new_objects)
        updates[path] = original
    original_interactions = page.get("visualInteractions", [])
    excluded = {
        (source, "bfiScenarioLift") for source in ("bfiCohort", "bfiCapacity", "bfiPeriod", "bfiDailyYield")
    }
    excluded.update(("bfiScenarioLift", item["name"]) for item in new_visuals if item["name"] != "bfiScenarioLift")
    excluded.update(("bfiScenarioLift", read_json(path)["name"]) for path in cards.values())
    retired = existing.keys() - managed
    page["visualInteractions"] = [
        interaction for interaction in original_interactions
        if (interaction["source"], interaction["target"]) not in excluded
        and interaction["source"] not in retired and interaction["target"] not in retired
    ] + [{"source": source, "target": target, "type": "NoFilter"} for source, target in sorted(excluded)]
    # Restrict the shared calendar on this page while keeping the date slicer interactive.
    filters = page.setdefault("filterConfig", {}).setdefault("filters", [])
    date_field = field("DimDate", "Date")
    date_filter = filter_for("DimDate", {"Between": {
        "Expression": field("DimDate", "Date", alias="f"),
        "LowerBound": {"Literal": {"Value": "datetime'2018-09-01T00:00:00.0000000'"}},
        "UpperBound": {"Literal": {"Value": "datetime'2018-09-30T00:00:00.0000000'"}},
    }})
    matching_filters = [item for item in filters if item.get("field") == date_field]
    if not existing and not matching_filters:
        filters.append({
            "name": uuid4().hex[:20], "field": date_field, "type": "Advanced", "isLockedInViewMode": True,
            "filter": date_filter,
        })
    elif not existing or len(matching_filters) != 1:
        raise ValueError("Unexpected page date filters. Inspect the saved report before applying.")
    page.update(width=1280, height=720, displayOption="FitToPage")
    if dark:
        page["displayName"] = TRIAGE_NAME
        page.setdefault("objects", {})["background"] = formatting(
            color=colour(CANVAS), transparency=literal("0D"),
        )
    shutil.copytree(page_path, staged_path)
    write_json(staged_path / "page.json", page)
    for key in retired:
        shutil.rmtree(staged_path / existing[key].parent.relative_to(page_path))
    for path, content in updates.items():
        write_json(staged_path / path.relative_to(page_path), content)
    for item in new_visuals:
        if item["name"] in existing:
            continue
        target = staged_path / "visuals" / item["name"] / "visual.json"
        target.parent.mkdir()
        write_json(target, item)


def stage_logo(report, staging):
    manifest = report / "definition" / "report.json"
    updated = read_json(manifest)
    packages = updated.setdefault("resourcePackages", [])
    matches = [package for package in packages if package["name"] == "RegisteredResources"]
    if len(matches) > 1 or (matches and matches[0]["type"] != "RegisteredResources"):
        raise ValueError("Unexpected RegisteredResources entries in the report.")
    if not matches:
        package = {"name": "RegisteredResources", "type": "RegisteredResources", "items": []}
        packages.append(package)
    else:
        package = matches[0]
    items = package.setdefault("items", [])
    entry = {"name": LOGO_NAME, "path": LOGO_NAME, "type": "Image"}
    occupied = [item for item in items if LOGO_NAME in (item["name"], item["path"])]
    if occupied and occupied != [entry]:
        raise ValueError(f"The logo resource name is already in use: {LOGO_NAME}")
    image = report / "StaticResources" / "RegisteredResources" / LOGO_NAME
    if image.exists() and not image.is_file():
        raise ValueError(f"The logo resource path is occupied: {image}.")
    data = LOGO_SOURCE.read_bytes()
    if image.exists() and image.read_bytes() != data:
        raise ValueError(f"A different image already exists at {image}.")
    if not occupied:
        items.append(entry)
    staged_manifest = staging / "updated-report.json"
    write_json(staged_manifest, updated)
    staged_image = staging / "updated-logo.png"
    staged_image.write_bytes(data)
    return manifest, image, staged_manifest, staged_image


def apply_page(page, staged, work, logo):
    backup = work / "original-page"
    created_image = False
    manifest_replaced = False
    if logo:
        manifest, image, staged_manifest, staged_image = logo
        shutil.copy2(manifest, work / "original-report.json")
        if not image.exists():
            (work / "logo-added.txt").write_text(LOGO_NAME + "\n", encoding="utf-8")
        image.parent.mkdir(parents=True, exist_ok=True)
    page.rename(backup)
    try:
        if logo:
            if not image.exists():
                staged_image.rename(image)
                created_image = True
            staged_manifest.replace(manifest)
            manifest_replaced = True
        staged.rename(page)
    except OSError as error:
        try:
            if manifest_replaced:
                shutil.copy2(work / "original-report.json", manifest)
            if created_image:
                image.unlink()
            backup.rename(page)
        except OSError as recovery_error:
            raise OSError(f"Automatic rollback failed. Recover from {work}: {recovery_error}") from error
        raise
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_folder", type=Path, help="The .Report folder inside the local PBIP copy")
    parser.add_argument("--apply", action="store_true", help="Apply the layout and retain the original page as a backup")
    parser.add_argument("--design", choices=("light", "fraud-triage"), default="light",
                        help="Choose the existing light layout or the dark Fraud Triage layout")
    args = parser.parse_args()
    report = args.report_folder.resolve()
    local_output = Path(__file__).resolve().parents[1] / "data" / "processed"
    if not report.is_relative_to(local_output):
        parser.error("Save a Power BI Project copy under this repository's data/processed folder.")
    if report.suffix != ".Report" or not (report / "definition.pbir").is_file():
        parser.error("Choose the folder ending in .Report beside the saved .pbip file.")

    try:
        dark = args.design == "fraud-triage"
        names = {PAGE_NAME, TRIAGE_NAME} if dark else {PAGE_NAME}
        pages = [
            path.parent for path in (report / "definition" / "pages").glob("*/page.json")
            if read_json(path).get("displayName") in names
        ]
        if len(pages) != 1:
            raise ValueError(f"Expected one PBIR page named {' or '.join(sorted(names))}.")
        page = pages[0]
        with_backup = Path(mkdtemp(prefix="bfi-review-layout-", dir=report.parent))
        staged = with_backup / "staged"
        try:
            build_page(page, staged, dark=dark)
            logo = stage_logo(report, with_backup) if dark else None
            if not args.apply:
                print(f"Preview passed: ready to apply the {args.design} layout.")
                return
            backup = apply_page(page, staged, with_backup, logo)
            print(f"Layout applied. Original page backup: {backup}")
        finally:
            if not (with_backup / "original-page").exists():
                shutil.rmtree(with_backup)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Layout could not be applied: {error}\n")


if __name__ == "__main__":
    main()
