import json
from pathlib import Path
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections
from graphify.report import generate

FIXTURES = Path(__file__).parent / "fixtures"

def make_inputs():
    extraction = json.loads((FIXTURES / "extraction.json").read_text())
    G = build_from_json(extraction)
    communities = cluster(G)
    cohesion = score_all(G, communities)
    labels = {cid: f"Community {cid}" for cid in communities}
    gods = god_nodes(G)
    surprises = surprising_connections(G)
    detection = {"total_files": 4, "total_words": 62400, "needs_graph": True, "warning": None}
    return G, communities, cohesion, labels, gods, surprises, detection

def test_report_contains_header():
    G, communities, cohesion, labels, gods, surprises, detection = make_inputs()
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, "./project")
    assert "# Graph Report" in report

def test_report_contains_corpus_check():
    G, communities, cohesion, labels, gods, surprises, detection = make_inputs()
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, "./project")
    assert "## Corpus Check" in report

def test_report_contains_god_nodes():
    G, communities, cohesion, labels, gods, surprises, detection = make_inputs()
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, "./project")
    assert "## God Nodes" in report

def test_report_contains_surprising_connections():
    G, communities, cohesion, labels, gods, surprises, detection = make_inputs()
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, "./project")
    assert "## Surprising Connections" in report

def test_report_contains_communities():
    G, communities, cohesion, labels, gods, surprises, detection = make_inputs()
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, "./project")
    assert "## Communities" in report

def test_report_contains_ambiguous_section():
    G, communities, cohesion, labels, gods, surprises, detection = make_inputs()
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, "./project")
    assert "## Ambiguous Edges" in report

def test_report_omits_token_cost():
    G, communities, cohesion, labels, gods, surprises, detection = make_inputs()
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, "./project")
    assert "Token " + "cost" not in report

def test_report_shows_raw_cohesion_scores():
    G, communities, cohesion, labels, gods, surprises, detection = make_inputs()
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, "./project")
    assert "Cohesion:" in report
    assert "✓" not in report
    assert "⚠" not in report
