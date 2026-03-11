// Page setup
#set page(margin: (x: 0.4in, y: 0.35in), paper: "us-letter")
#set text(size: 10.5pt)
#set par(justify: true)

// Color theme
#let accent = rgb("#bb0000")
#let link-color = rgb("#333333")

// Typography constants
#let name-size = 20pt
#let section-size = 12pt
#let secondary-size = 10pt

// Spacing constants
#let section-gap = 4pt
#let section-rule-offset = -3pt
#let section-post-rule = 2pt
#let entry-gap = 1pt
#let grid-gutter = 8pt
#let edu-row-gutter = 3pt
#let skills-gutter = 10pt

// List formatting
#let list-indent = 8pt
#let list-body-indent = 3pt

// Helper: secondary text (italic, smaller)
#let secondary(body) = text(style: "italic", size: secondary-size)[#body]

// Helper: skill category label (bold, smaller)
#let skill-label(body) = text(weight: "bold", size: secondary-size)[#body]

// Helper: bullet list with consistent indentation
#let cv-list(..items) = list(indent: list-indent, body-indent: list-body-indent, ..items)

// Custom header — compact single-line contact rows
#align(center)[
  #text(size: name-size, weight: "bold")[Robert A. Frenken] \
  #v(2pt)
  #text(size: secondary-size)[
    ✉ #link("mailto:frenken.2@osu.edu")[frenken.2\@osu.edu] · 📍 Columbus, OH · 🌐 #link("https://robertfrenken.github.io")[robertfrenken.github.io]
  ]
  #text(size: secondary-size)[
    💻 #link("https://github.com/RobertFrenken")[GitHub] · 💼 #link("https://www.linkedin.com/in/robert-frenken/")[LinkedIn] · 🎓 #link("https://scholar.google.com/citations?user=_VbkYiwAAAAJ")[Google Scholar]
  ]
]

#v(section-gap)

// Helper function for section headings — tighter spacing
#let section(title) = {
  v(section-gap)
  text(size: section-size, weight: "bold", fill: accent)[#upper(title)]
  v(section-rule-offset)
  line(length: 100%, stroke: 0.5pt + accent)
  v(section-post-rule)
}

// Helper for CV entries: title on left, date on right — tighter spacing
#let entry(title, org, date) = {
  grid(
    columns: (1fr, auto),
    column-gutter: grid-gutter,
    text(weight: "bold", size: 10.5pt)[#title],
    secondary[#date],
  )
  if org != none {
    secondary[#org]
  }
  v(entry-gap)
}

// Make all links use link-color
#show link: set text(fill: link-color)

#section("Education")

#text(weight: "bold", size: 10.5pt)[The Ohio State University] #h(1fr) #secondary[Columbus, OH]
#v(1pt)
#grid(
  columns: (1fr, auto),
  row-gutter: edu-row-gutter,
  [Ph.D. in Industrial & Systems Engineering], align(right)[#secondary[August 2021 – Present]],
  [M.S. in Industrial & Systems Engineering], align(right)[#secondary[May 2024]],
  [B.S. in Industrial & Systems Engineering], align(right)[#secondary[May 2021]],
)
#v(section-post-rule)
#skill-label[MS GPA: 3.83 / BS GPA: 3.63]

#section("Professional Experience")

#entry("Graduate Research Assistant", "Ohio State University", "2021 – Present")

#secondary[Center for Automotive Research (2024 – Present)]
#cv-list(
  [Developing a classification model for distinguishing attack-free and malicious messages within a CAN bus system. This supervised ensemble model combines VGAE and GAT.],
  [Created a federated learning testing bed configurable to be either centralized or decentralized, with the ability to change dataset, model, graph topology, and aggregation strategy.],
)

#secondary[Spine Research Institute (2021 – 2024)]
#cv-list(
  [Created multiple supervised and unsupervised machine learning models to classify lower back pain from wearable data of over 1000 participants. The supervised ensemble CNN model achieved 90% accuracy.],
)

#entry("Data Science Intern", "Ford Motor Co. | Columbus, OH (Remote)", "2020")

#cv-list(
  [Leveraged HPC tools (Spark, Hadoop, HIVE, SQL) and Python to query, merge, and aggregate trip data.],
  [Developed a decision tree model analyzing the correlation between oil life efficiency and warranty repair rates.],
)

#entry("Machine Learning Research Assistant", "Ohio State University", "2020 – 2021")

#cv-list(
  [Built web-scraping program to automate extraction of weekly FanDuel player metrics. Conducted clustering and sentiment analysis to inform lineup decisions.],
)

#entry("Quality Systems Data Analyst Co-op", "Momentive", "2019")
Built Python/Excel data pipeline for HVAC metrics, production yields, and machine reliability tracking.

#entry("Project Engineering Co-op", "DuPont", "2018")
Executed 12 capital projects (\$1M+ total), averaging 10% under budget. Installed roller lifts, pallet yards, and pumps.

#section("Publications")

#cv-list(
  [*R Frenken*, SG Bhatti, H Zhang, Q Ahmed (2025) "KD-GAT: Combining Knowledge Distillation and Graph Attention Transformer for a Controller Area Network Intrusion Detection System" _IEEE ITSC_ (to appear).],
  [*R Frenken*, SG Bhatti, H Zhang, Q Ahmed (2025) "Multi-Stage Knowledge-Distilled VGAE and GAT for Robust Controller-Area-Network Intrusion Detection" (preprint).],
)

#section("Projects")

#entry("Ohio Campaign Finance Dashboard", none, "2026 – Present")
Interactive data visualization platform (#link("https://ohtransparencymaps.com")[ohtransparencymaps.com]) exploring political contributions and spending across Ohio legislative districts. Built with D3.js, DuckDB-WASM, and Observable Framework. Features 6 pages with 18+ chart types (choropleths, Sankey diagrams, network graphs), real-time filtering across 28K+ contribution records, and LLM-assisted donor/expenditure classification.

#entry("Center for AI Safety (CAIS) 2025 Capstone Project", none, "2025")
C Leet, *R Frenken*. Tacit Coordination: Coordination without Communication — empirical investigation of LLM behavior in game-theoretic scenarios (prisoner's dilemma, battle-of-the-sexes, duopoly markets).

#entry("Mobility Systems Lab Documentation", none, "2026 – Present")
Creator and maintainer of the lab's technical knowledge base (#link("https://osu-car-msl.github.io/lab-setup-guide/")[osu-car-msl.github.io/lab-setup-guide]). Onboarding resource covering HPC workflows, PyTorch/PyG setup, SLURM job management, and ML best practices — reducing new student ramp-up time and serving as a persistent reference for the research group.

#section("Skills & Training")

#grid(
  columns: (auto, 1fr),
  column-gutter: skills-gutter,
  row-gutter: edu-row-gutter,
  skill-label[ML/DL:],
  [PyTorch, PyTorch Geometric, Ray, scikit-learn, Weights & Biases],
  skill-label[Data:],
  [DuckDB, Spark, Hadoop, SQL, Pandas, NumPy],
  skill-label[Infrastructure:],
  [AWS, Azure, SLURM, Git, Linux],
  skill-label[Languages:],
  [Python, Java, SQL, MATLAB, HTML/CSS],
  skill-label[Coursework:],
  [High Performance Computing, Nonconvex Optimization, Computer Vision, Human Centered ML, Reinforcement Learning, Data Mining, Machine Learning, Data Structures & Algorithms, Database Design, Linear & Non Linear Programming, Statistics.],
)

#section("Service & Mentorship")

*Reviewer:* ITSC 2025, AAAI 2025

*Mentorship:*
- #link("https://www.linkedin.com/in/hanqin-zhang-5610a1280/")[Hanqin Zhang] — B.S. Computer Science '25, Ohio State · now M.S. Georgia Tech
- #link("https://dralston168.github.io/")[Drew Ralston] — B.S. Computer Science '28 (expected), Ohio State
- #link("https://gugu-12.github.io/")[Chunyu Gu] — B.S. Mathematics '28 (expected), Ohio State
