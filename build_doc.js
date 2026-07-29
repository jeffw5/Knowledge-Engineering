const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, PageBreak, TableOfContents, LevelFormat, convertInchesToTwip,
  Header, Footer, PageNumber, ExternalHyperlink
} = require("docx");

const DIA = "/sessions/eloquent-determined-fermi/mnt/outputs/diagrams/";
const NAVY = "1F3A5F";
const GOLD = "B8860B";
const GREEN = "2E7D4F";
const GRAY = "555555";
const LIGHTGRAY = "F2F4F7";

function img(file, width, height) {
  return new ImageRun({
    type: "png",
    data: fs.readFileSync(DIA + file),
    transformation: { width, height },
  });
}

function figure(file, width, height, caption) {
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 80 },
      children: [img(file, width, height)],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 240 },
      children: [new TextRun({ text: caption, italics: true, size: 18, color: GRAY })],
    }),
  ];
}

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 400, after: 160 }, children: [new TextRun(text)] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 300, after: 120 }, children: [new TextRun(text)] });
}
function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160 },
    children: Array.isArray(text) ? text : [new TextRun({ text, ...opts })],
  });
}
function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 80 },
    children: Array.isArray(text) ? text : [new TextRun(text)],
  });
}
function bold(text) { return new TextRun({ text, bold: true }); }
function italic(text) { return new TextRun({ text, italics: true, color: GRAY }); }

function cell(children, opts = {}) {
  return new TableCell({
    width: { size: opts.width || 2000, type: WidthType.DXA },
    shading: opts.shading ? { type: ShadingType.CLEAR, fill: opts.shading } : undefined,
    margins: { top: 100, bottom: 100, left: 120, right: 120 },
    verticalAlign: "center",
    children: Array.isArray(children) ? children : [new Paragraph({ children: [new TextRun({ text: children, bold: opts.bold, color: opts.color, size: opts.size })] })],
  });
}

function headerCell(text, width) {
  return cell(new Paragraph({ children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 20 })] }), { width, shading: NAVY });
}
function bodyCell(text, width, opts = {}) {
  return cell(new Paragraph({ children: [new TextRun({ text, size: 19, ...opts })] }), { width, shading: opts.shading });
}

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 21 } },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: NAVY, font: "Calibri" },
        paragraph: { spacing: { before: 400, after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 25, bold: true, color: NAVY, font: "Calibri" },
        paragraph: { spacing: { before: 300, after: 120 } } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, color: GOLD, font: "Calibri" },
        paragraph: { spacing: { before: 200, after: 100 } } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 260 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 820, hanging: 260 } } } },
      ]},
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC", space: 4 } },
            children: [new TextRun({ text: "Untangling Legacy Logic: an SSOT Architecture", size: 16, color: "888888" })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "Page ", size: 16, color: "888888" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "888888" })],
          })],
        }),
      },
      children: [
        // ---------------- Title Page ----------------
        new Paragraph({ spacing: { before: 1600 }, children: [] }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Untangling Scattered Business Logic", bold: true, size: 52, color: NAVY })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 200, after: 100 },
          children: [new TextRun({ text: "An Architecture for a Single Source of Truth Across Code, Rules Engines, and Ontologies", size: 28, color: GOLD, bold: true })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 400 },
          children: [new TextRun({ text: "Architecture Proposal — Domain-Centric Metadata & Execution-Translation Pipeline", size: 22, color: GRAY, italics: true })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 1200 },
          children: [new TextRun({ text: "Prepared for internal architecture review", size: 20, color: GRAY })],
        }),
        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- Executive Summary ----------------
        h1("Executive Summary"),
        p([
          new TextRun("Business logic in most enterprises is scattered across legacy code, database triggers, rules engine UIs, and informal ontologies — with no single place that tells you what the system actually does, or why. The result is "),
          bold("logic drift"),
          new TextRun(": the same rule re-implemented three different ways, each drifting further from the others with every change."),
        ]),
        p("This proposal lays out an architecture that fixes the root cause rather than the symptom. Two ideas do the work:"),
        bullet([bold("A domain-centric Single Source of Truth (SSOT)."), new TextRun(" Every constraint, rule, and computation is defined once, in a declarative spec, under version control.")]),
        bullet([bold("An explicit execution-translation pipeline."), new TextRun(" A CI/CD build step compiles that one spec into whatever each runtime needs — typed code, semantic graph artifacts, or rules-engine XML — instead of forcing every runtime to speak the same language.")]),
        p([
          new TextRun("The architecture is deliberately "),
          bold("not"),
          new TextRun(" a call to replace legacy engines with one universal tool. It treats business logic as a governed, versioned data artifact, and lets code, rules engines, and ontologies keep doing what each does best."),
        ]),

        // ---------------- Problem ----------------
        h1("The Problem: Logic Has No Fixed Address"),
        p("Legacy estates accumulate three failure modes simultaneously, and they compound each other:"),
        bullet([bold("Duplication."), new TextRun(" The same eligibility rule lives in a stored procedure, a Drools ruleset, and a service-layer if-statement — each maintained independently.")]),
        bullet([bold("Silent drift."), new TextRun(" A rule changes in one place during an incident fix and is never propagated to the other two.")]),
        bullet([bold("No audit trail."), new TextRun(" Rules engine UIs and database triggers are edited directly in production, with no PR, no review, and no version history.")]),
        p([
          new TextRun("The instinctive fix — pick one tool and force everything into it — reliably fails. Procedural algorithms don't belong in a rules engine, and stateful workflows don't belong in an ontology. Section 1 gives each kind of logic its correct home before anything is centralized."),
        ]),
        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- Section 1 ----------------
        h1("1. Classify Logic by Layer — the “Right Home” Principle"),
        p([
          new TextRun("Before centralizing anything, classify what kind of logic you're looking at. Mixing these categories — running procedural code inside an ontology, or building stateful algorithms inside a rules engine — is the single largest driver of legacy bloat."),
        ]),
        ...figure("d1_classification.png", 600, 220, "Figure 1. Three logic categories, each routed to the tool built for its paradigm."),
        h3Table([
          ["Category", "Governing question", "Best-fit tooling", "Example"],
          ["Constraints\n(structural / semantic)", "What must always be true about the domain data?", "Ontologies (OWL/RDF); schema definitions (JSON Schema, OpenAPI, Pydantic, Protobuf)", "An Order must have at least one Line Item, and the Customer must exist."],
          ["Business Rules\n(policy / decision)", "What actions or decisions occur based on state?", "Rules engines (Drools, Camunda, DMN) or a DSL", "If customer tier is Gold and order total > $100, apply a 15% discount."],
          ["Computational Logic\n(procedural / algorithmic)", "How is state computed or processed sequentially?", "Code — microservices, DDD domain services", "Route optimization, or a multi-step ML feature pipeline."],
        ]),

        // ---------------- Section 2 ----------------
        h1("2. Treat Logic as Code — the Governance Pipeline"),
        p([
          new TextRun("Once logic is classified, it needs a "),
          bold("Single Source of Truth"),
          new TextRun(": a central repository holding logic specs in human-readable form (YAML, DMN, Turtle/OWL). The hard rule that makes this work: "),
          bold("nobody edits a rule directly in a Rules Engine UI or a production database."),
          new TextRun(" Everything is checked into source control first, and reaches production only by passing through CI."),
        ]),
        h2("Continuous Integration for Logic"),
        p("Rule and schema changes go through the same discipline as application code:"),
        bullet([bold("Linting & validation."), new TextRun(" Semantic reasoners (e.g., HermiT) catch contradictory ontology axioms; static analysis catches malformed or conflicting DMN tables before merge.")]),
        bullet([bold("Automated unit & scenario testing."), new TextRun(" Rule changes run against synthetic datasets pre-deployment, to catch side effects a human reviewer would miss.")]),
        bullet([bold("Semantic versioning."), new TextRun(" Rule sets and schemas are versioned explicitly. Consuming microservices declare which version of a policy or schema they depend on, so a rule change cannot silently break a downstream consumer.")]),
        ...figure("d2_governance.png", 480, 395, "Figure 2. The GitOps loop for logic: commit → CI validation → gated release → versioned consumption, with rejected changes routed back to the author."),

        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- Section 3 ----------------
        h1("3. The Modern Pattern: Declarative Spec + Generated Executables"),
        p([
          new TextRun("Rather than rewriting legacy applications to “speak the same language,” the architecture is "),
          bold("declarative-first"),
          new TextRun(": logic is written once, and a build pipeline compiles it down to whatever each target runtime needs."),
        ]),
        ...figure("d3_compile_targets.png", 600, 240, "Figure 3. One declarative spec, three generated runtime artifacts, one CI/CD compiler in between."),
        h2("How it works"),
        bullet([bold("Write once, declaratively."), new TextRun(" Schema constraints, taxonomy, and core decisions are defined in standardized formats — OpenAPI/JSON Schema for constraints, DMN for rules.")]),
        bullet([bold("Compile for runtimes."), new TextRun(" Code generators in CI/CD produce the target artifacts on every merge:")]),
        bullet("TypeScript/Python interfaces for microservices", 1),
        bullet("SHACL/OWL files for the semantic graph store", 1),
        bullet("DMN/Drools XML for the rules-engine runtime", 1),
        p([
          new TextRun("Because all three artifacts regenerate from the same versioned spec on every build, they cannot drift out of sync with each other — drift becomes a build failure, not a production incident."),
        ]),

        // ---------------- Decision API runtime view ----------------
        h2("Runtime View: The Decision API"),
        p([
          new TextRun("At request time, callers don't talk to the rules engine, the ontology store, or a legacy stored procedure directly. They talk to a "),
          bold("standardized Decision API"),
          new TextRun(" that resolves the caller's declared policy version, validates the request against the current schema, and routes to whichever backend currently owns that decision — including a wrapped legacy engine that hasn't been migrated yet."),
        ]),
        ...figure("d5_decision_api.png", 560, 328, "Figure 4. A client microservice never calls the rules engine, ontology store, or legacy procedure directly — it calls the Decision API, which is free to route to legacy or modern backends without the client knowing which."),
        p([
          new TextRun("This indirection is what makes the migration in Section 4 possible: the facade lets legacy and modernized decision logic sit behind one interface, so callers never need to change when the backend behind that interface changes."),
        ]),

        new Paragraph({ children: [new PageBreak()] }),

        // ---------------- Section 4 ----------------
        h1("4. Practical Migration Blueprint for Legacy Systems"),
        p("For logic trapped in stored procedures, hardcoded Java/COBOL, and legacy rules engines, migrate in three phases rather than attempting a rewrite:"),
        h2("Phase 1 — Logic Discovery & Extraction"),
        bullet([bold("Inventory & audit."), new TextRun(" Map existing logic with tracing tools and static analysis. Log every point where a business decision is made.")]),
        bullet([bold("Classify."), new TextRun(" Sort each finding into Constraint, Rule, or Computation using the framework in Section 1.")]),
        h2("Phase 2 — Decouple via API Boundaries (Strangler Fig)"),
        bullet([bold("Wrap, don't rewrite."), new TextRun(" Put legacy rules engines and stored procedures behind the standardized Decision API from Section 3 before touching their internals.")]),
        bullet([bold("Extract incrementally."), new TextRun(" Pull hardcoded logic out of application code into externalized configuration or DMN files piece by piece, re-pointing the facade as each piece lands.")]),
        h2("Phase 3 — Centralize Schemas First"),
        bullet([bold("Standardize data shapes."), new TextRun(" Unify data definitions across teams via a common ontology or schema registry before consolidating rules.")]),
        bullet([bold("Consolidate rules second."), new TextRun(" Once the underlying data definitions (constraints) are unified, reconciling the business rules that operate on that data becomes dramatically simpler — most apparent rule conflicts turn out to be data-shape conflicts in disguise.")]),
        ...figure("d4_migration.png", 600, 261, "Figure 5. Three-phase strangler-fig migration: discover and classify, decouple behind a Decision API, then centralize schemas before consolidating rules."),

        // ---------------- Pitfalls ----------------
        h1("Key Pitfalls to Avoid"),
        pitfallsTable(),

        // ---------------- Recommendations ----------------
        h1("Recommended Next Steps"),
        bullet([bold("Stand up the SSOT repository and CI pipeline first"), new TextRun(" — before extracting a single rule. Governance has to exist before there's anything worth governing.")]),
        bullet([bold("Pilot on one bounded decision"), new TextRun(" (e.g., discount eligibility) to prove the classify → spec → compile → deploy loop end-to-end, including the Decision API facade.")]),
        bullet([bold("Inventory before you migrate."), new TextRun(" Run Phase 1 across the legacy estate broadly before committing engineering time to Phase 2 extraction — classification changes the shape of the migration plan.")]),
        bullet([bold("Make version declaration mandatory"), new TextRun(" for any service consuming a policy or schema from day one, so the versioning discipline never has retrofitting debt.")]),
      ],
    },
  ],
});

function h3Table(rows) {
  const widths = [1700, 2400, 2900, 2360];
  const header = new TableRow({
    tableHeader: true,
    children: rows[0].map((t, i) => headerCell(t, widths[i])),
  });
  const body = rows.slice(1).map((r, idx) =>
    new TableRow({
      children: r.map((t, i) =>
        cell(
          t.split("\n").map((line, li) => new Paragraph({ spacing: { after: li === t.split("\n").length - 1 ? 0 : 40 }, children: [new TextRun({ text: line, size: 18, bold: i === 0 })] })),
          { width: widths[i], shading: idx % 2 === 0 ? "F7F9FB" : undefined }
        )
      ),
    })
  );
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: widths,
    rows: [header, ...body],
  });
}

function pitfallsTable() {
  const widths = [2600, 6760];
  const data = [
    ["The “Universal Engine” Trap", "Don't run procedural code inside an ontology, or build complex stateful algorithms inside a rules engine. Use each tool for the paradigm it was built for — see Section 1."],
    ["Unversioned Database Triggers", "Move validation logic out of SQL triggers and into upstream microservices or declarative schema checks, where it can be versioned, tested, and reviewed."],
    ["Orphaned Rule Authoring", "Avoid business-user UIs that save directly to production databases without passing through Git and CI testing first — this is the single fastest way to reintroduce logic drift."],
  ];
  const header = new TableRow({
    tableHeader: true,
    children: [headerCell("Pitfall", widths[0]), headerCell("Why it matters / what to do instead", widths[1])],
  });
  const body = data.map(([a, b], idx) =>
    new TableRow({
      children: [
        cell(new Paragraph({ children: [new TextRun({ text: a, bold: true, size: 19, color: "B03A2E" })] }), { width: widths[0], shading: idx % 2 === 0 ? "FBEAEA" : "FFF5F5" }),
        cell(new Paragraph({ children: [new TextRun({ text: b, size: 19 })] }), { width: widths[1], shading: idx % 2 === 0 ? "FBEAEA" : "FFF5F5" }),
      ],
    })
  );
  return new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: widths, rows: [header, ...body] });
}

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("/sessions/eloquent-determined-fermi/mnt/outputs/SSOT_Logic_Architecture.docx", buf);
  console.log("written");
});
