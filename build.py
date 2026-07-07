# Static-site generator for primum.co.za — run `python build.py` to regenerate
# all pages from the shared template. No dependencies.
import io, json

SITE = "https://www.primum.co.za"
EMAIL = "admin@primum.co.za"
PHONE = "073 653 1650"          # confirmed 2026-07-07; linked to WhatsApp
PHONE_INTL = "+27736531650"
ADDRESS = "Tijger Vallei, Silver Lakes, Pretoria"
HPCSA = "HPCSA MP0867748"
HOURS = "Mon–Thu 08:00–16:00 · Fri 08:00–13:00 · Weekends & public holidays closed"

PAGES = {
    "index.html":     ("Home", "/"),
    "employers.html": ("For Employers", "/employers.html"),
    "practices.html": ("For Medical Practices", "/practices.html"),
    "schemes.html":   ("For Schemes & Insurers", "/schemes.html"),
    "members.html":   ("For Patients & Members", "/members.html"),
    "about.html":     ("About", "/about.html"),
    "contact.html":   ("Contact", "/contact.html"),
    "privacy.html":   ("Privacy (POPIA)", "/privacy.html"),
}

def header(active):
    links = [
        ("index.html", "Home"), ("employers.html", "Employers"),
        ("practices.html", "Practices"), ("schemes.html", "Schemes"),
        ("members.html", "Members"), ("about.html", "About"),
    ]
    nav = "".join(
        f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>'
        for h, t in links
    )
    return f'''<header>
  <div class="nav-wrap">
    <a class="brand" href="index.html">
      <img src="assets/logo.jpg" alt="Primum Health Group logo">
      <span><span class="brand-name">Primum Health Group</span><br><span class="brand-sub">Occupational Health &middot; Care Coordination</span></span>
    </a>
    <nav class="main-nav">{nav}<a class="cta" href="contact.html">Contact us</a></nav>
  </div>
</header>'''

FOOTER = f'''<footer>
  <div class="footer-inner">
    <div>
      <h4>Primum Health Group</h4>
      <p>Occupational health and care-coordination practice serving employers, medical practices, schemes, insurers and their members across South Africa.</p>
      <p class="tagline-sm">We turn cover into care.</p>
    </div>
    <div>
      <h4>Who we serve</h4>
      <ul>
        <li><a href="employers.html">Employers</a></li>
        <li><a href="practices.html">Medical practices</a></li>
        <li><a href="schemes.html">Schemes, insurers &amp; funders</a></li>
        <li><a href="members.html">Patients &amp; members</a></li>
      </ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul>
        <li><a href="about.html">About us</a></li>
        <li><a href="contact.html">Contact</a></li>
        <li><a href="privacy.html">Privacy &amp; POPIA</a></li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <ul>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="https://wa.me/27736531650">{PHONE} (WhatsApp)</a></li>
        <li>{ADDRESS}</li>
        <li style="font-size:.78rem;color:#64748b">{HOURS}</li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 Primum Health Group. All rights reserved.</span>
    <span>Registered healthcare practice &middot; {HPCSA} &middot; POPIA compliant</span>
  </div>
</footer>'''

REVEAL_JS = '''<script>
(function(){
  var els = document.querySelectorAll('.card, .band, .cta-strip, .panel-dark, details.faq');
  els.forEach(function(el){ el.classList.add('reveal'); });
  if (!('IntersectionObserver' in window)) { els.forEach(function(el){ el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  els.forEach(function(el){ io.observe(el); });
})();
</script>'''

def breadcrumb_ld(fname):
    if fname == "index.html":
        return None
    return {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": PAGES[fname][0], "item": SITE + PAGES[fname][1]},
      ],
    }

def page(fname, title, desc, body, jsonld=None, active=None):
    lds = list(jsonld or [])
    bc = breadcrumb_ld(fname)
    if bc:
        lds.append(bc)
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in lds)
    html = f'''<!DOCTYPE html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{PAGES[fname][1]}">
<link rel="icon" type="image/jpeg" href="assets/logo.jpg">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{PAGES[fname][1]}">
<meta property="og:image" content="{SITE}/assets/logo.jpg">
<meta property="og:locale" content="en_ZA">
<meta property="og:site_name" content="Primum Health Group">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="geo.region" content="ZA-GP">
<meta name="geo.placename" content="Pretoria">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
{ld}
</head>
<body>
{header(active or fname)}
<main>
{body}
</main>
{FOOTER}
{REVEAL_JS}
</body>
</html>'''
    io.open(fname, "w", encoding="utf-8", newline="\n").write(html)
    print("wrote", fname)

ORG_LD = {
  "@context": "https://schema.org",
  "@type": "MedicalBusiness",
  "name": "Primum Health Group",
  "url": SITE,
  "logo": f"{SITE}/assets/logo.jpg",
  "email": EMAIL,
  "telephone": PHONE_INTL,
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Tijger Vallei, Silver Lakes",
    "addressLocality": "Pretoria",
    "addressRegion": "Gauteng",
    "addressCountry": "ZA"
  },
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"], "opens": "08:00", "closes": "16:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "13:00"}
  ],
  "founder": {"@type": "Person", "name": "Dr A Nazo", "jobTitle": "Founder & Principal Practitioner", "identifier": "HPCSA MP0867748"},
  "areaServed": "ZA",
  "description": "South African occupational-health and care-coordination practice. We manage employee and patient populations for employers, medical practices and schemes — turning each member's actual medical-aid benefits into a scheduled, billable year plan of care.",
  "medicalSpecialty": ["Occupational medicine", "Preventive medicine", "Community health"],
  "knowsAbout": ["Occupational health", "COIDA compliance", "Medical incapacity assessment", "Care coordination", "Chronic disease management", "Prescribed Minimum Benefits", "Oncology care pathways", "Employee wellness"]
}

def faq_ld(pairs):
    return {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in pairs
      ]
    }

def faqs_html(pairs):
    return "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs)

# ─────────────────────────── HOME ───────────────────────────
home_faqs = [
  ("What does Primum Health Group do?",
   "Primum Health Group is a South African occupational-health and care-coordination practice. We run workplace health programmes for employers (medicals, surveillance, COIDA, incapacity management) and coordinate ongoing healthcare for patient populations — building each member a year plan of screenings, chronic-care visits and tests based on what their medical aid actually covers, with the correct billing codes ready for the treating doctor."),
  ("What is care coordination?",
   "Care coordination means one accountable team makes sure every patient actually receives the care they are due — the right screenings for their age and gender, the right chronic-disease check-ups for their conditions, at the right time — and that every visit is billed correctly to the medical scheme benefit that must pay for it, not the member's pocket."),
  ("Who does Primum work with?",
   "Employers who need occupational health and employee wellness; GP and specialist practices who want their patient base proactively managed; medical schemes, health insurers and other healthcare funders seeking managed care — active chronic disease management, prevention programmes and population health management with coordination across providers; and the members themselves."),
]
home = f'''
<section class="hero">
  <div class="hero-inner">
    <span class="kicker">Occupational Health &middot; Care Coordination &middot; Population Health</span>
    <h1>You carry people who count on you. <em>We make sure none of them slip through.</em></h1>
    <p class="lead">A workforce. A practice full of patients. A scheme's members. Your own family. Primum Health Group is the care-coordination partner behind you — turning every person's actual medical-aid benefits into a scheduled, billable year plan of care, so the people you're responsible for get what they're due, on time, every year.</p>
    <div class="actions">
      <a class="btn btn-gold" href="contact.html">Talk to us</a>
      <a class="btn btn-ghost" href="#how">How it works</a>
    </div>
    <p class="tagline">Cover is not care. We turn cover into care.</p>
  </div>
</section>

<section id="how">
  <div class="section-inner">
    <p class="eyebrow">Who we stand behind</p>
    <h2 class="section-title">You're the hero of this story. We're the guide.</h2>
    <p class="section-sub">Healthcare fails in the gaps between employer, doctor, scheme and member. Whichever of these you are, our job is to hand you the plan, the codes and the follow-through that let you win.</p>
    <div class="grid grid-2">
      <div class="card"><span class="tag">You, the employer</span><h3>You protect a workforce. We arm you for it.</h3><p>You answer for every fitness certificate, every injury on duty, every incapacity case. We give you medicals, surveillance, COIDA claims handled end to end, and a wellness programme your auditors and your people both respect.</p><ul class="checks"><li>Fitness certificates &amp; risk-based surveillance</li><li>COIDA compliance and claims, end to end</li><li>Absenteeism &amp; incapacity, defensibly managed</li></ul><p style="margin-top:.8rem"><a href="employers.html"><b>For employers →</b></a></p></div>
      <div class="card"><span class="tag">You, the doctor</span><h3>You carry the patients. We carry the coordination.</h3><p>You became a doctor to treat people — not to chase recalls and decode benefit rules. We tell you who is due, for what, with the exact tariff and ICD-10 codes ready for your billing system.</p><ul class="checks"><li>Year plans per patient, by age, gender &amp; diagnosis</li><li>Claim-ready referrals — tariff + ICD-10 in claim order</li><li>Recalls, reminders and results follow-up handled</li></ul><p style="margin-top:.8rem"><a href="practices.html"><b>For practices →</b></a></p></div>
      <div class="card"><span class="tag">You, the funder</span><h3>You fund the cover. We turn it into care.</h3><p>For medical schemes, health insurers and other healthcare funders we run managed care that actually lands: active chronic-disease management, prevention programmes, and population-health management with care coordination across providers.</p><ul class="checks"><li>Active chronic disease management (CDL and beyond)</li><li>Prevention &amp; screening programmes members actually use</li><li>Population health management — coordinated across providers</li></ul><p style="margin-top:.8rem"><a href="schemes.html"><b>For schemes &amp; insurers →</b></a></p></div>
      <div class="card"><span class="tag">You &amp; your family</span><h3>You look after everyone else. Who's watching your health?</h3><p>Serious illness rarely announces itself in time. We watch for you and your dependants — screenings on schedule, chronic conditions controlled, problems caught while they're still small.</p><ul class="checks"><li>Your plan's benefits, actually used</li><li>Your dependants covered — children to grandparents</li><li>Cancer support before, during and after treatment</li></ul><p style="margin-top:.8rem"><a href="members.html"><b>For members →</b></a></p></div>
    </div>

    <div class="band">
      <div class="stat"><b>27 chronic conditions</b><span>PMB Chronic Disease List coordinated, plus scheme-specific extended lists</span></div>
      <div class="stat"><b>Schemes · insurers · funders</b><span>Managed care for medical schemes, health insurance products and other healthcare funders — Discovery, Bonitas, GEMS, Polmed, Momentum, Medshield, Affinity and more</span></div>
      <div class="stat"><b>Billing-code ready</b><span>Every activity carries the tariff code and ICD-10 in claim order</span></div>
      <div class="stat"><b>POPIA compliant</b><span>Role-based access, audit-trailed, consent-first data handling</span></div>
    </div>

    <div class="cta-strip">
      <div><h3>See what coordinated care looks like for your people.</h3><p>Employers, practices and funders: book a walkthrough of our platform and pathways.</p></div>
      <a class="btn btn-navy" href="contact.html">Book a conversation</a>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="section-inner">
    <h2 class="section-title">Common questions</h2>
    {faqs_html(home_faqs)}
  </div>
</section>
'''
page("index.html",
     "Primum Health Group — Occupational Health & Care Coordination, South Africa",
     "South African occupational-health and care-coordination practice. We manage employee and patient populations for employers, practices and schemes — year plans, correct billing, better outcomes.",
     home, [ORG_LD, faq_ld(home_faqs)])

# ─────────────────────── EMPLOYERS ───────────────────────
emp_faqs = [
  ("What occupational health services do employers get?",
   "Pre-employment, periodic and exit medicals; fitness-for-duty certificates; medical surveillance programmes matched to your risk exposures; COIDA (Workmen's Compensation) compliance and claims management; and medical incapacity and disability assessments with defensible reports."),
  ("What is COIDA claims management?",
   "When an employee is injured on duty, we handle the Compensation for Occupational Injuries and Diseases Act process end to end — first medical reports, ongoing treatment coordination, final assessments and disability ratings — so the claim is compliant and the employee returns to work safely."),
  ("How does employee wellness work on a per-member basis?",
   "Your workforce is enrolled as a managed population. Every employee gets an annual wellness assessment and a personal year plan; those with chronic conditions get structured care. You get aggregate reporting — never individual medical detail without consent — at a predictable per-member monthly rate."),
]
employers = f'''
<div class="page-hero"><div class="section-inner"><h1>Workplace health that protects your people — and your compliance file</h1><p>From fitness certificates to COIDA claims to a managed employee-wellness population: one accountable practice, predictable costs, defensible paperwork.</p></div></div>
<section><div class="section-inner">
  <div class="grid grid-3">
    <div class="card"><span class="tag">Medicals</span><h3>Occupational medicals &amp; surveillance</h3><ul class="checks"><li>Pre-employment, periodic &amp; exit medicals</li><li>Fitness-for-duty certificates</li><li>Risk-based surveillance (audiometry, spirometry, vision)</li><li>Legal-register-aligned programmes</li></ul></div>
    <div class="card"><span class="tag">COIDA</span><h3>Injury-on-duty &amp; claims</h3><ul class="checks"><li>COIDA registration &amp; compliance</li><li>First medical &amp; progress reports</li><li>Claims submission &amp; follow-through</li><li>Return-to-work coordination</li></ul></div>
    <div class="card"><span class="tag">Incapacity</span><h3>Incapacity &amp; disability assessment</h3><ul class="checks"><li>Medical incapacity evaluations</li><li>Disability ratings &amp; reports</li><li>Case management with HR &amp; insurers</li><li>Medico-legal grade documentation</li></ul></div>
  </div>
  <div class="card" style="margin-top:1.2rem"><span class="tag">Population wellness</span><h3>Your workforce as a managed health population</h3><p>Beyond compliance: we enrol your employees into coordinated care. Every member gets an annual wellness check and a year plan; chronic conditions get proper ongoing management; screenings their medical aid already pays for actually happen. You see the aggregate picture — participation, risk trends, absenteeism drivers — at a predictable per-member monthly rate.</p></div>
  <div class="cta-strip"><div><h3>Get a workplace-health proposal</h3><p>Tell us your headcount and industry — we'll map the programme and the price.</p></div><a class="btn btn-navy" href="contact.html">Request a proposal</a></div>
  <h2 class="section-title" style="margin-top:2.6rem">Employer questions</h2>
  {faqs_html(emp_faqs)}
</div></section>
'''
page("employers.html",
     "Occupational Health for Employers — COIDA, Medicals, Incapacity | Primum Health Group",
     "Occupational medicals, surveillance, COIDA claims management, incapacity assessments and managed employee-wellness populations for South African employers.",
     employers, [faq_ld(emp_faqs)])

# ─────────────────────── PRACTICES ───────────────────────
pr_faqs = [
  ("What does Primum actually do for my practice?",
   "We coordinate your patient population on your behalf. Every chronic and screening-eligible patient gets a year plan built from their actual medical-aid benefits; we handle recalls and reminders; and you receive referrals listing exactly who is due, for what, with the tariff codes and ICD-10 codes ready to capture in your billing system."),
  ("How do the billing codes work?",
   "Every activity we schedule carries the procedure/tariff code and the ICD-10 codes in the correct claim order — PMB codes first, so chronic and oncology claims route to the scheme's risk pool instead of the member's savings. Your reception captures the claim exactly as printed on our referral."),
  ("Does this cost my practice anything?",
   "The model is simple: your patients get more of the care they are already entitled to, your practice bills for that care, and the coordination is funded through the population arrangement. We'll walk you through the numbers for your patient base."),
]
practices = f'''
<div class="page-hero"><div class="section-inner"><h1>We tell you who is due, for what — with the billing codes ready</h1><p>Your patients, proactively managed. Chronic check-ups, screenings and pathway care scheduled for the whole practice population — and every referral arrives claim-ready.</p></div></div>
<section><div class="section-inner">
  <div class="grid grid-3">
    <div class="card"><span class="tag">Year plans</span><h3>A plan per patient</h3><p>Built from age, gender, diagnoses and — crucially — what the patient's specific plan option actually covers, across Discovery, Bonitas, GEMS, Polmed, Momentum, Medshield and Affinity.</p></div>
    <div class="card"><span class="tag">Claim-ready referrals</span><h3>Codes, not guesswork</h3><p>Tariff code + ICD-10 in claim order on every line. PMB codes first so chronic care hits the risk pool. A printable billing quick-reference for your front desk.</p></div>
    <div class="card"><span class="tag">Follow-through</span><h3>Recalls &amp; results, handled</h3><p>We chase the recalls, remind the patients, track the results, and flag what needs your clinical attention — so no chronic patient quietly falls out of care.</p></div>
  </div>
  <div class="card" style="margin-top:1.2rem"><span class="tag">Clinical pathways</span><h3>Oncology prehab &amp; rehab, ERAS-aligned</h3><p>For patients diagnosed with cancer, we run a structured pathway anchored to the treatment date: prehabilitation (anaemia correction, nutrition, exercise, cessation, stoma education), perioperative coordination, recovery, and five-year surveillance — every activity billable, every code verified. Colorectal follows the full ERAS surgical protocol; other tumours run a structured oncology backbone.</p></div>
  <div class="cta-strip"><div><h3>See a sample year plan and referral</h3><p>Bring one anonymised patient profile — we'll show you the plan and the claim lines.</p></div><a class="btn btn-navy" href="contact.html">Book a demo</a></div>
  <h2 class="section-title" style="margin-top:2.6rem">Practice questions</h2>
  {faqs_html(pr_faqs)}
</div></section>
'''
page("practices.html",
     "Care Coordination for Medical Practices — Claim-Ready Referrals | Primum Health Group",
     "We manage your patient population: year plans per patient, recalls handled, referrals with tariff and ICD-10 codes ready for your billing system.",
     practices, [faq_ld(pr_faqs)])

# ─────────────────────── SCHEMES ───────────────────────
sc_faqs = [
  ("What managed-care services does Primum provide to funders?",
   "Four core services for medical schemes, health insurers and other healthcare funders: active chronic disease management (members managed to protocol, not just registered), prevention and screening programmes that members actually use, population health management across your book, and care coordination across the providers who treat your members."),
  ("How does coordination help a scheme or insurer?",
   "Members who receive their preventive screenings and structured chronic care cost less over time and claim more correctly. We drive utilisation of the benefits you already fund — screening baskets, chronic programmes, oncology benefits — with PMB-correct coding that keeps claims clean."),
  ("What is PMB-correct claiming?",
   "Prescribed Minimum Benefit conditions must by law be funded from scheme risk. We ensure every chronic and oncology claim carries the PMB ICD-10 code in the primary position, so claims route correctly the first time — fewer rejections, fewer member complaints, cleaner data."),
  ("Do you only work with medical schemes?",
   "No — we provide managed care for medical schemes, health insurance products and other healthcare funders: employer self-funded arrangements, bargaining-council funds and administrators. The coordination model adapts to each funding environment."),
]
schemes = f'''
<div class="page-hero"><div class="section-inner"><h1>Managed care for medical schemes, health insurers &amp; healthcare funders</h1><p>You fund the cover. We turn it into care: active chronic disease management, prevention programmes, and population health management with care coordination across providers — so benefit design becomes member outcomes.</p></div></div>
<section><div class="section-inner">
  <div class="grid grid-2">
    <div class="card"><span class="tag">Managed care</span><h3>Active chronic disease management</h3><p>Not a register — a programme. Every chronic member managed to protocol: the right visits, the right tests, at the right cadence, with correct combination coding and DSP alignment. All 27 PMB CDL conditions plus scheme-specific extended lists.</p></div>
    <div class="card"><span class="tag">Prevention</span><h3>Prevention programmes that get used</h3><p>Age- and gender-appropriate screening scheduled for every eligible member — mammography, cervical, colorectal, PSA, HIV, wellness checks — against each option's actual benefit rules. Utilisation, not wastage.</p></div>
    <div class="card"><span class="tag">Population health</span><h3>Population health management</h3><p>Your whole book, stratified and managed: prevention for the well, structured care for the chronic, pathways for the acutely ill — with reporting that shows movement, not just membership.</p></div>
    <div class="card"><span class="tag">Coordination</span><h3>Care coordination across providers</h3><p>GPs, specialists, pathology, radiology, allied health — your member's care joined up across all of them, referrals claim-ready, results followed through. Includes ERAS-aligned oncology prehab, rehab and five-year surveillance pathways.</p></div>
  </div>
  <div class="cta-strip"><div><h3>Pilot a population with us</h3><p>Pick a cohort — an employer group or a chronic register — and measure the difference.</p></div><a class="btn btn-navy" href="contact.html">Start the conversation</a></div>
  <h2 class="section-title" style="margin-top:2.6rem">Funder questions</h2>
  {faqs_html(sc_faqs)}
</div></section>
'''
page("schemes.html",
     "Managed Care for Medical Schemes & Health Insurers | Primum Health Group",
     "Managed care for medical schemes, health insurers and healthcare funders: active chronic disease management, prevention programmes, population health management and care coordination across providers.",
     schemes, [faq_ld(sc_faqs)])

# ─────────────────────── MEMBERS ───────────────────────
me_faqs = [
  ("What do I get as a member?",
   "A personal year plan: the check-ups, screenings, blood tests and chronic-care visits you and your dependants should have this year, scheduled month by month — with reminders. Much of it is already paid for by your medical aid; we make sure you actually receive it."),
  ("Does my medical aid pay for this care?",
   "Most of what we schedule is covered: preventive screenings from your plan's screening benefit, chronic care from the Chronic Disease List benefit the law requires your scheme to fund, and cancer care from the oncology benefit. Where something is not covered, we tell you the cost upfront — no surprises."),
  ("What happens if something IS found?",
   "That's exactly when you want us at your side. We coordinate the whole journey — the specialist referrals, the scheme authorisations, the treatment pathway, the follow-up schedule — so you can focus on getting well while we handle the system."),
  ("Are my children and dependants included?",
   "Yes. Your whole family on the plan is enrolled: childhood immunisation schedules, teenage and adult screenings, chronic care for a parent — everyone registered as your dependant is watched over."),
  ("Is my health information safe?",
   "Yes. We are POPIA compliant: your information is processed with your consent, access is role-based and audit-trailed, and we never share individual medical details with your employer."),
]
members = f'''
<div class="page-hero"><div class="section-inner"><h1>You look after everyone else. We look after you — and everyone you love on your plan.</h1><p>A personal year plan of check-ups, screenings and chronic care for you and your dependants, built from what your medical aid actually covers. We watch the calendar so you never have to wonder.</p></div></div>
<section><div class="section-inner">

  <div class="panel-dark">
    <p class="eyebrow" style="color:#e8c766">The uncomfortable truth</p>
    <h3>The most dangerous conditions are the <em>quiet</em> ones.</h3>
    <p>High blood pressure doesn't hurt — until the stroke. Diabetes doesn't hurt — until the kidneys, the eyes, the foot. Most cancers grow silently for years; found early they are often treatable, found late the options narrow fast. And the cruellest part? The screenings that catch these early are usually <b>already paid for by your medical aid</b> — they just never get booked. Missed check-ups don't feel like a risk. Until the year one of them mattered.</p>
    <div class="assure">
      <p><b style="color:#e8c766">This is what we take off your shoulders.</b> When you and your family are enrolled with Primum, someone is watching: every screening booked when it's due, every chronic condition tracked to target, every result followed up, every dependant — from your youngest child's immunisations to your parents' heart checks — on a schedule. If something is ever found, it's found <b>early</b>, and you won't face the system alone: we coordinate the specialists, the authorisations and the treatment pathway around you.</p>
    </div>
  </div>

  <div class="grid grid-3">
    <div class="card"><span class="tag">Prevention</span><h3>Caught early, not late</h3><p>The right screening for your age and stage — wellness checks, mammograms, pap smears, colon screening, PSA, HIV testing — booked on time, mostly free under your plan's screening benefit.</p></div>
    <div class="card"><span class="tag">Chronic care</span><h3>The quiet conditions, watched</h3><p>Blood pressure, diabetes, cholesterol, asthma, HIV and 20+ other chronic conditions monitored to protocol — so the silent ones never get the years they need to do damage.</p></div>
    <div class="card"><span class="tag">Cancer support</span><h3>Never alone in the system</h3><p>If cancer is found, a structured pathway wraps around you: getting you strong before surgery, supporting recovery after, and five years of vigilant follow-up — coordinated for you, step by step.</p></div>
  </div>
  <div class="cta-strip"><div><h3>Put your family on a watch list — the good kind.</h3><p>Join through your employer, your doctor's practice — or directly as an individual member.</p></div><a class="btn btn-navy" href="contact.html">Get in touch</a></div>
  <h2 class="section-title" style="margin-top:2.6rem">Member questions</h2>
  {faqs_html(me_faqs)}
</div></section>
'''
page("members.html",
     "Care Coordination for Patients & Members | Primum Health Group",
     "A personal year plan of screenings, check-ups and chronic care built from your medical-aid benefits — with reminders so nothing gets missed.",
     members, [faq_ld(me_faqs)])

# ─────────────────────── ABOUT ───────────────────────
about = f'''
<div class="page-hero"><div class="section-inner"><h1>Primary health. Occupational health. Medico-legal. Coordinated.</h1><p>Primum Health Group is a doctor-led South African practice built on a simple conviction: most of the care people need is already funded — it just never gets coordinated. We fix that.</p></div></div>
<section><div class="section-inner">
  <div class="grid grid-2">
    <div class="card"><h3>What we believe</h3><p>Benefits without coordination are promises without delivery. A member with diabetes is entitled by law to structured chronic care; a 50-year-old is entitled to cancer screening; an injured worker is entitled to a properly managed COIDA claim. Our job is to make entitlement become appointment — scheduled, delivered, correctly billed.</p></div>
    <div class="card"><h3>How we work</h3><p>Our own care-coordination platform understands the benefit rules of South Africa's major schemes and options, generates a year plan per member, and produces claim-ready referrals for treating providers. Clinical pathways follow published guidelines (ERAS, NCCN/ESMO); billing follows verified tariff conventions; data handling follows POPIA.</p></div>
    <div class="card"><h3>Leadership — Dr A Nazo, Founder &amp; Principal Practitioner</h3>
      <p>Dr Nazo built Primum on a conviction formed in Eastern Cape communities where care too often arrived late or not at all: <b>our clients are the heroes of this story</b> — the employer protecting a workforce, the practice carrying a patient community, the funder stretching every benefit rand, the member facing a diagnosis. They don't need rescuing; they need a capable guide. Primum exists to be that guide — the plan, the coordination and the follow-through that let our clients win.</p>
      <p style="margin-top:.7rem">In practice that means speaking each client's language: OHSA and COIDA compliance for employers, sustainable practice economics for doctors, value-based outcomes and clean claims for funders, and dignity for every member — with accountability in writing for the care that follows. <span style="color:#64748b">HPCSA MP0867748.</span></p></div>
    <div class="card"><h3>Credentials</h3><ul class="checks"><li>Registered practitioner: {HPCSA}</li><li>Practice: {ADDRESS}</li><li>POPIA-compliant systems: role-based access, audit trail, consent-first</li><li>Funders worked with: Discovery, Bonitas, GEMS, Polmed, Momentum, Medshield, Affinity — among other schemes, insurers and healthcare funders</li></ul></div>
  </div>
</div></section>
'''
page("about.html",
     "About Primum Health Group — Doctor-Led Care Coordination, South Africa",
     "A doctor-led South African practice combining occupational health, primary care coordination and medico-legal work — delivered through our own POPIA-compliant platform.",
     about, [ORG_LD])

# ─────────────────────── CONTACT ───────────────────────
contact = f'''
<div class="page-hero"><div class="section-inner"><h1>Talk to us</h1><p>Employers, practices, funders and members — tell us who you are and what you need; we respond within one business day.</p></div></div>
<section><div class="section-inner">
  <div class="grid grid-2">
    <div class="card">
      <h3>Direct contact</h3>
      <ul class="checks">
        <li>Email: <a href="mailto:{EMAIL}"><b>{EMAIL}</b></a></li>
        <li>Phone / WhatsApp: <a href="https://wa.me/27736531650"><b>{PHONE}</b></a></li>
        <li>Practice address: <b>{ADDRESS}</b></li>
        <li>Hours: {HOURS}</li>
      </ul>
      <p style="margin-top:.9rem;font-size:.85rem;color:#64748b">Existing coordination clients: your care coordinator remains your first contact.</p>
    </div>
    <div class="card">
      <h3>What to include</h3>
      <ul class="checks">
        <li><b>Employers:</b> headcount, industry, sites, current occ-health arrangements</li>
        <li><b>Practices:</b> practice size, patient-base profile, billing system used</li>
        <li><b>Funders:</b> the population or register you'd like to pilot</li>
        <li><b>Members:</b> your scheme &amp; option name (no medical details by email, please)</li>
      </ul>
    </div>
  </div>
</div></section>
'''
page("contact.html",
     "Contact Primum Health Group",
     "Contact Primum Health Group — occupational health and care coordination. Email admin@primum.co.za or WhatsApp us.",
     contact, [ORG_LD])

# ─────────────────────── PRIVACY ───────────────────────
privacy = f'''
<div class="page-hero"><div class="section-inner"><h1>Privacy &amp; POPIA</h1><p>How Primum Health Group processes personal and special personal information under the Protection of Personal Information Act, 2013.</p></div></div>
<section><div class="section-inner">
  <div class="card">
    <h3>Our commitments</h3>
    <ul class="checks">
      <li><b>Lawful basis first.</b> Health information is special personal information; we process it with your explicit consent (or another lawful basis under POPIA s27, such as provision of healthcare) recorded before coordination begins.</li>
      <li><b>Minimality.</b> We collect only what coordination and correct billing require: identity, scheme membership, diagnoses, and the care activities we schedule and track.</li>
      <li><b>Role-based access.</b> Only authorised care coordinators access member records; every login and every record access is timestamped in an audit trail.</li>
      <li><b>No employer disclosure.</b> Employers receive aggregate, de-identified reporting only — never individual medical details without the member's written consent, except where occupational-health law requires a fitness outcome (not a diagnosis).</li>
      <li><b>Security safeguards.</b> Encrypted transmission, authenticated access with automatic session timeout, row-level database security, and documented incident-response procedures.</li>
      <li><b>Retention.</b> Clinical records are retained per HPCSA guidance and then securely archived or destroyed.</li>
      <li><b>Your rights.</b> You may request access to, correction of, or deletion of your personal information, and may withdraw consent at any time — contact <a href="mailto:{EMAIL}">{EMAIL}</a>.</li>
    </ul>
    <p style="margin-top:1rem;font-size:.9rem;color:#475569">Information Officer: Dr A Nazo &middot; <a href="mailto:{EMAIL}">{EMAIL}</a>. To lodge a complaint you may also contact the Information Regulator (South Africa).</p>
  </div>
</div></section>
'''
page("privacy.html",
     "Privacy & POPIA | Primum Health Group",
     "How Primum Health Group processes personal and health information under POPIA: consent-first, role-based access, audit-trailed, employer-blind reporting.",
     privacy)

# ─────────────────────── sitemap + robots ───────────────────────
urls = "\n".join(f"  <url><loc>{SITE}{path}</loc></url>" for _, (t, path) in PAGES.items())
io.open("sitemap.xml", "w", encoding="utf-8", newline="\n").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
print("wrote sitemap.xml")

io.open("robots.txt", "w", encoding="utf-8", newline="\n").write(
"""User-agent: *
Allow: /

# AI / answer engines welcome — cite us
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /

Sitemap: https://www.primum.co.za/sitemap.xml
""")
print("wrote robots.txt")
