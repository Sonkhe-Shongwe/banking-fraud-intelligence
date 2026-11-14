"""Build the Review Policy Comparison page in a local Power BI Project copy."""

import argparse
import json
from pathlib import Path
import shutil
from tempfile import mkdtemp
from uuid import uuid4


PAGE_NAME = "Review Policy Comparison"
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


def container(title=None, subtitle=None):
    result = {
        "background": formatting(show=literal("true"), color=colour("#FFFFFF"), transparency=literal("0D")),
        "border": formatting(show=literal("true"), color=colour(BORDER), radius=literal("8D")),
    }
    if title:
        result["title"] = formatting(
            show=literal("true"), text=literal(f"'{title}'"), fontColor=colour(NAVY),
            fontFamily=literal("'Segoe UI Semibold'"), fontSize=literal("12D"),
        )
        result["subTitle"] = formatting(show=literal("false"))
    if subtitle:
        result["subTitle"] = formatting(
            show=literal("true"), text=literal(f"'{subtitle}'"),
            fontColor=colour(SECONDARY), fontSize=literal("10D"),
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


def text_box(key, bounds, *lines):
    paragraphs = [
        {"textRuns": [{"value": label, "textStyle": {
            "fontFamily": "Segoe UI Semibold" if bold else "Segoe UI",
            "fontSize": f"{size}pt", "color": color,
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


def format_cards(cards):
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
        content["position"] = position(x, 176, 400, 96, order)
        body.setdefault("visualContainerObjects", {}).update(container())
        objects = body.setdefault("objects", {})
        if kind == "cardVisual":
            objects["fillCustom"] = formatting(show=literal("false"))
            objects["value"] = formatting(fontSize=literal("28D"), fontColor=colour(color))
            objects["label"] = formatting(show=literal("true"), fontSize=literal("11D"))
        else:
            objects["labels"] = formatting(fontSize=literal("28D"), color=colour(color))
            objects["categoryLabels"] = formatting(show=literal("true"), fontSize=literal("11D"))
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


def build_page(page_path, staged_path):
    page = read_json(page_path / "page.json")
    new_visuals = supporting_visuals()
    visual_files = sorted(page_path.glob("visuals/*/visual.json"))
    managed = {item["name"] for item in new_visuals}
    existing = {path.parent.name: path for path in visual_files if path.parent.name in managed}
    cards = matching_cards([path for path in visual_files if path not in existing.values()])
    updates = format_cards(cards)
    if len(visual_files) != len(cards) + len(existing) or (existing and existing.keys() != managed):
        raise ValueError("Expected the original three-card page or the complete page generated by this builder.")
    for item in new_visuals:
        path = existing.get(item["name"])
        if path is None:
            continue
        original = read_json(path)
        body = original["visual"]
        updated = item["visual"]
        if original["name"] != item["name"] or body["visualType"] != updated["visualType"]:
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
        if item["name"] in {"bfiCohort", "bfiCapacity", "bfiPeriod"}:
            new_objects.pop("general", None)
        body.setdefault("objects", {}).update(new_objects)
        updates[path] = original
    original_interactions = page.get("visualInteractions", [])
    excluded = {
        (source, "bfiScenarioLift") for source in ("bfiCohort", "bfiCapacity", "bfiPeriod", "bfiDailyYield")
    }
    excluded.update(("bfiScenarioLift", item["name"]) for item in new_visuals if item["name"] != "bfiScenarioLift")
    excluded.update(("bfiScenarioLift", read_json(path)["name"]) for path in cards.values())
    page["visualInteractions"] = [
        interaction for interaction in original_interactions
        if (interaction["source"], interaction["target"]) not in excluded
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
    shutil.copytree(page_path, staged_path)
    write_json(staged_path / "page.json", page)
    for path, content in updates.items():
        write_json(staged_path / path.relative_to(page_path), content)
    for item in new_visuals:
        if item["name"] in existing:
            continue
        target = staged_path / "visuals" / item["name"] / "visual.json"
        target.parent.mkdir()
        write_json(target, item)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_folder", type=Path, help="The .Report folder inside the local PBIP copy")
    parser.add_argument("--apply", action="store_true", help="Apply the layout and retain the original page as a backup")
    args = parser.parse_args()
    report = args.report_folder.resolve()
    local_output = Path(__file__).resolve().parents[1] / "data" / "processed"
    if not report.is_relative_to(local_output):
        parser.error("Save a Power BI Project copy under this repository's data/processed folder.")
    if report.suffix != ".Report" or not (report / "definition.pbir").is_file():
        parser.error("Choose the folder ending in .Report beside the saved .pbip file.")

    try:
        pages = [
            path.parent for path in (report / "definition" / "pages").glob("*/page.json")
            if read_json(path).get("displayName") == PAGE_NAME
        ]
        if len(pages) != 1:
            raise ValueError(f"Expected one PBIR page named {PAGE_NAME}.")
        page = pages[0]
        with_backup = Path(mkdtemp(prefix="bfi-review-layout-", dir=report.parent))
        staged = with_backup / "staged"
        try:
            build_page(page, staged)
            if not args.apply:
                print("Preview passed: ready to apply the comparison page layout.")
                return
            backup = with_backup / "original-page"
            page.rename(backup)
            try:
                staged.rename(page)
            except OSError:
                backup.rename(page)
                raise
            print(f"Layout applied. Original page backup: {backup}")
        finally:
            if not (with_backup / "original-page").exists():
                shutil.rmtree(with_backup)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Layout could not be applied: {error}\n")


if __name__ == "__main__":
    main()
