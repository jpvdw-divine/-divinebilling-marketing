"""Public SA business guides (www.divinebilling.online/guides).

Written to be quoted: each guide opens with standalone key takeaways, keeps one
claim per sentence, dates its review, and links the primary source (SARS, PSIRA).
When a rule changes, update the text AND the `reviewed` date.
"""

REVIEWED = '2026-10-09'

GUIDES = [
    {
        'slug': 'emp201-paye-uif-sdl',
        'title': 'EMP201 explained: monthly PAYE, UIF and SDL for South African employers',
        'seo_title': 'EMP201 guide: PAYE, UIF & SDL deadlines (2026)',
        'meta': ('What goes on the SARS EMP201, when it is due, how UIF and SDL are calculated, '
                 'and how the monthly returns reconcile to the EMP501. Reviewed October 2026.'),
        'summary': 'The monthly employer return: what it contains, when it is due and how to stay reconciled.',
        'dept': 'payroll',
        'published': '2026-10-09',
        'reviewed': REVIEWED,
        'takeaways': [
            'The EMP201 is the monthly SARS declaration of PAYE, UIF and SDL an employer owes for the previous month.',
            'It must be filed and paid within seven days after the end of the month in which the tax was deducted — by the 7th.',
            'If the 7th falls on a weekend or public holiday, the deadline moves to the last business day before it.',
            'UIF is 2% in total: 1% deducted from the employee and 1% paid by the employer, on remuneration up to R17 712 a month.',
            'SDL is 1% of total remuneration, payable by employers whose annual payroll exceeds R500 000.',
            'The monthly EMP201s must reconcile to the EMP501: an interim reconciliation for March–August and an annual one for the full tax year.',
        ],
        'sections': [
            ('What is the EMP201?',
             '<p>The EMP201 is the monthly employer declaration submitted to the South African Revenue Service (SARS). '
             'It declares three amounts for the previous calendar month: employees’ tax (PAYE) withheld from salaries, '
             'Unemployment Insurance Fund (UIF) contributions, and the Skills Development Levy (SDL). Each EMP201 '
             'generates a payment reference number (PRN) that you use to pay SARS.</p>'
             '<p>Any employer registered for PAYE files an EMP201 every month, including months in which no '
             'payroll was run — in that case you submit a nil return.</p>'),
            ('When is the EMP201 due?',
             '<p>SARS requires payment within seven days after the end of the month in which the amounts were '
             'deducted. In practice that means <strong>the 7th of the following month</strong>: September payroll is '
             'due by 7 October.</p>'
             '<p>When the 7th falls on a weekend or public holiday, the deadline moves <em>earlier</em>, to the last '
             'business day before it — not later. For example, 7 November 2026 is a Saturday, so the October 2026 '
             'EMP201 is due on Friday 6 November 2026.</p>'
             '<p>Late payment attracts penalties and interest, so most employers file and pay a few days before '
             'the 7th to allow for bank clearing.</p>'),
            ('How PAYE, UIF and SDL are calculated',
             '<ul>'
             '<li><strong>PAYE</strong> is withheld from each employee’s remuneration using the SARS tax tables or '
             'the annualised calculation method, after allowing for rebates and deductions such as retirement '
             'fund contributions.</li>'
             '<li><strong>UIF</strong> is 1% of the employee’s remuneration deducted from their pay, plus a matching '
             '1% from the employer. Contributions are calculated on remuneration up to the ceiling of R17 712 a '
             'month, so the maximum is R177.12 from each side (R354.24 in total) per employee per month.</li>'
             '<li><strong>SDL</strong> is 1% of the total remuneration paid to all employees. It is payable only if '
             'the employer’s annual payroll exceeds (or is expected to exceed) R500 000. SDL is an employer cost; '
             'it is never deducted from employees.</li>'
             '</ul>'),
            ('Step by step: filing a monthly EMP201',
             '<ol class="steps">'
             '<li>Finalise the month’s payroll: hours, overtime, allowances, leave and terminations.</li>'
             '<li>Total PAYE, employee and employer UIF, and SDL from the payslips.</li>'
             '<li>Capture the totals on the EMP201 on SARS eFiling (or e@syFile) and submit it.</li>'
             '<li>Pay the amount using the PRN on the return, before the due date.</li>'
             '<li>Keep the payslips, the EMP201 and proof of payment together: you will need them to reconcile.</li>'
             '</ol>'),
            ('Reconciling to the EMP501',
             '<p>Twice a year employers reconcile the monthly EMP201 declarations and payments to the tax '
             'certificates (IRP5 and IT3(a)) issued to employees, using the EMP501:</p>'
             '<ul>'
             '<li><strong>Interim reconciliation</strong> — covers 1 March to 31 August. For the 2027 '
             'reconciliation year SARS set the submission window as 21 September to 31 October 2026.</li>'
             '<li><strong>Annual reconciliation</strong> — covers the full tax year from 1 March to the end of '
             'February. The next window is 1 April to 31 May 2027.</li>'
             '</ul>'
             '<p>SARS imposes an administrative penalty of 1% of annual PAYE for a late EMP501, increasing by 1% '
             'for every month it remains outstanding, up to 10%. Mismatches usually come from a single month: a '
             'payment made without the correct PRN, a late-captured termination, or a manual adjustment that '
             'never reached the EMP201.</p>'),
            ('Common mistakes',
             '<ul>'
             '<li>Paying on the 7th when the 7th is a Saturday — the deadline was the Friday before.</li>'
             '<li>Deducting 2% UIF from the employee instead of 1% each.</li>'
             '<li>Calculating UIF on full salary above the R17 712 ceiling.</li>'
             '<li>Forgetting SDL once payroll grows past R500 000 a year.</li>'
             '<li>Treating long-term contractors as suppliers when SARS would regard them as employees — see '
             '<a href="/guides/contractor-invoicing-south-africa">paying contractors in South Africa</a>.</li>'
             '</ul>'),
        ],
        'faqs': [
            ('When is the EMP201 due?',
             'By the 7th of the month after the payroll month. If the 7th is a weekend or public holiday, it is '
             'due on the last business day before it.'),
            ('How much is UIF in South Africa?',
             '2% of remuneration: 1% deducted from the employee and 1% paid by the employer, calculated on '
             'remuneration up to R17 712 a month — a maximum of R177.12 each.'),
            ('Who has to pay SDL?',
             'Employers whose total annual payroll exceeds R500 000. SDL is 1% of total remuneration and is paid '
             'by the employer, not deducted from employees.'),
            ('Do I file an EMP201 if I did not run payroll?',
             'Yes. An employer registered for PAYE submits an EMP201 every month; in a month with no payroll it '
             'is a nil return.'),
        ],
        'sources': [
            ('SARS — Pay As You Earn (PAYE)', 'https://www.sars.gov.za/types-of-tax/pay-as-you-earn/'),
            ('SARS — Employer interim reconciliation, 21 September to 31 October 2026',
             'https://www.sars.gov.za/latest-news/employer-interim-declarations-emp501-21-september-to-october-2026/'),
        ],
        'product': ('DivineBilling Payroll runs pay runs and payslips and totals PAYE, employee and employer '
                    'UIF and SDL for each month’s EMP201, so the numbers you capture on eFiling come straight '
                    'from the payroll that produced them.'),
    },
    {
        'slug': 'vat-tax-invoice-requirements',
        'title': 'What a valid tax invoice needs in South Africa (2026)',
        'seo_title': 'SA tax invoice requirements & VAT thresholds (2026)',
        'meta': ('The particulars a SARS-valid tax invoice must show, full vs abridged invoices, the 21-day rule, '
                 'and the new R2.3 million VAT registration threshold from 1 April 2026.'),
        'summary': 'Full vs abridged tax invoices, the 21-day rule and the new VAT registration thresholds.',
        'dept': 'finance',
        'published': '2026-10-09',
        'reviewed': REVIEWED,
        'takeaways': [
            'The standard VAT rate in South Africa is 15%.',
            'From 1 April 2026 a business must register for VAT once taxable supplies exceed, or are expected to exceed, R2.3 million in 12 months (previously R1 million).',
            'Voluntary VAT registration is possible from R120 000 of taxable supplies in 12 months (previously R50 000).',
            'A full tax invoice is required when the consideration is more than R5 000; an abridged tax invoice is allowed at R5 000 or less.',
            'No tax invoice is required when the consideration is R50 or less; a till slip showing the VAT is enough.',
            'A tax invoice must be issued within 21 days of the supply, and without a valid tax invoice the buyer cannot claim input tax.',
        ],
        'sections': [
            ('VAT basics in 2026',
             '<p>Value-added tax in South Africa is charged at a standard rate of <strong>15%</strong>. Only a '
             'registered VAT vendor may charge VAT or issue a tax invoice.</p>'
             '<p>The registration thresholds changed on <strong>1 April 2026</strong>:</p>'
             '<ul>'
             '<li><strong>Compulsory registration</strong> — when taxable supplies exceed, or are reasonably expected '
             'to exceed, <strong>R2.3 million</strong> in any 12-month period (up from R1 million).</li>'
             '<li><strong>Voluntary registration</strong> — possible once taxable supplies exceed '
             '<strong>R120 000</strong> in 12 months (up from R50 000).</li>'
             '</ul>'
             '<p>Many guides written before 2026 still quote R1 million. If your turnover is between R1 million and '
             'R2.3 million, registration is now a choice rather than an obligation — speak to your accountant '
             'before deregistering, because input-tax and deregistration rules apply.</p>'),
            ('What a full tax invoice must show',
             '<p>SARS requires a full tax invoice when the consideration (price including VAT) is <strong>more than '
             'R5 000</strong>. It must show:</p>'
             '<ol>'
             '<li>The words “Tax Invoice”, “VAT Invoice” or “Invoice”.</li>'
             '<li>The supplier’s name, address and VAT registration number.</li>'
             '<li>The recipient’s name and address, and the recipient’s VAT registration number if the recipient '
             'is a vendor.</li>'
             '<li>A serial number and the date of issue.</li>'
             '<li>An accurate description of the goods or services, noting second-hand goods.</li>'
             '<li>The quantity or volume supplied.</li>'
             '<li>The value of the supply, the VAT charged and the total consideration.</li>'
             '</ol>'
             '<p>Missing the buyer’s VAT number is the most common reason SARS disallows an input-tax claim on an '
             'otherwise correct invoice.</p>'),
            ('Abridged tax invoices and small amounts',
             '<p>When the consideration is <strong>R5 000 or less</strong>, a vendor may issue an abridged tax '
             'invoice. It still identifies the supplier (name, address and VAT number), carries a serial number '
             'and date, describes the supply, and shows the consideration with either the VAT amount or a '
             'statement that VAT at 15% is included — but the buyer’s details are not required.</p>'
             '<p>When the consideration is <strong>R50 or less</strong>, no tax invoice is required. The buyer '
             'still needs a document such as a till slip showing the VAT charged to support an input-tax claim.</p>'),
            ('Timing, copies and credit notes',
             '<ul>'
             '<li>Issue the tax invoice within <strong>21 days</strong> of the supply.</li>'
             '<li>Issue only one original per supply. A replacement must be clearly marked “copy”.</li>'
             '<li>Correct an invoice with a credit or debit note — do not edit and re-send the original.</li>'
             '<li>Keep invoices for at least five years: SARS can ask for them in an audit.</li>'
             '</ul>'),
            ('Checklist before you send an invoice',
             '<ul>'
             '<li>Are you a registered vendor? If not, do not charge VAT or call it a tax invoice.</li>'
             '<li>Is the total over R5 000? Then include the buyer’s name, address and VAT number.</li>'
             '<li>Is the serial number unique and sequential?</li>'
             '<li>Do quantity × price, the VAT line and the total add up?</li>'
             '<li>Is it going out within 21 days of the supply?</li>'
             '</ul>'),
        ],
        'faqs': [
            ('What is the VAT registration threshold in South Africa?',
             'From 1 April 2026 registration is compulsory once taxable supplies exceed R2.3 million in 12 months. '
             'Voluntary registration is possible from R120 000. Before April 2026 the thresholds were R1 million '
             'and R50 000.'),
            ('When do I need a full tax invoice?',
             'When the consideration, including VAT, is more than R5 000. At R5 000 or less an abridged tax invoice '
             'is allowed, and at R50 or less no tax invoice is required.'),
            ('How long do I have to issue a tax invoice?',
             'A vendor must issue a tax invoice within 21 days of making the supply.'),
            ('Can a business that is not VAT registered issue a tax invoice?',
             'No. Only a registered VAT vendor may charge VAT or issue a tax invoice. A non-vendor issues an '
             'ordinary invoice without VAT.'),
        ],
        'sources': [
            ('SARS — Value-Added Tax (thresholds and rate)', 'https://www.sars.gov.za/types-of-tax/value-added-tax/'),
            ('SARS — Tax invoices', 'https://www.sars.gov.za/businesses-and-employers/government/tax-invoices/'),
        ],
        'product': ('DivineBilling issues numbered tax invoices and quotes with your VAT number, the customer’s '
                    'VAT details and 15% VAT lines, keeps credit notes linked to the original, and logs every '
                    'change for audit.'),
    },
    {
        'slug': 'contractor-invoicing-south-africa',
        'title': 'Paying contractors in South Africa: invoices, PAYE risk and VAT',
        'seo_title': 'Paying contractors in SA: invoices, PAYE & VAT',
        'meta': ('When SARS treats a contractor as an employee, what a contractor invoice must contain, when a '
                 'contractor may charge VAT, and a clean workflow from timesheet to payment.'),
        'summary': 'How to keep contractors genuinely independent, invoice them correctly and pay them safely.',
        'dept': 'finance',
        'published': '2026-10-09',
        'reviewed': REVIEWED,
        'takeaways': [
            'SARS looks at how the work is actually done, not at what the contract calls the person.',
            'If you control and supervise how, when and where someone works, SARS may treat their pay as remuneration — and expect you to have withheld PAYE.',
            'Payments to a company or trust can also attract PAYE if it is a “personal service provider” — essentially an employee working through an entity.',
            'A contractor may only charge VAT if they are a registered VAT vendor; registration is compulsory above R2.3 million of taxable supplies in 12 months.',
            'Labour law has a separate test: section 200A of the Labour Relations Act presumes employment when certain indicators are present for workers earning below the earnings threshold.',
            'Pay against an approved invoice and verified bank details, never against an email request to change banking details.',
        ],
        'sections': [
            ('Contractor or employee? Why it matters',
             '<p>Businesses use contractors for flexibility: guards on extra sites, technicians, consultants, '
             'drivers. The risk is that a “contractor” who works like an employee is treated as one. If SARS '
             'decides a payment was remuneration, the business that paid it is liable for the PAYE it should have '
             'withheld, plus penalties and interest — and the contractor may have UIF and labour-law claims.</p>'),
            ('Signs SARS will see an employee',
             '<p>SARS weighs the substance of the relationship. Indicators that point towards employment:</p>'
             '<ul>'
             '<li>You decide how, when and where the work is done, and supervise it.</li>'
             '<li>The work is performed mainly at your premises, on your schedule.</li>'
             '<li>The person is paid for time worked rather than for a defined result.</li>'
             '<li>They work only for you, use your tools, and cannot send someone else in their place.</li>'
             '</ul>'
             '<p>Indicators of a genuine independent contractor point the other way: their own tools and premises, '
             'several clients, payment for a deliverable, freedom to subcontract, and carrying their own business '
             'risk. No single factor decides it.</p>'
             '<p>If the contractor invoices through a company or trust that is effectively one person doing '
             'employee-like work for you, it may be a <strong>personal service provider</strong>, and PAYE must be '
             'withheld from payments to it. SARS sets out its view in Interpretation Note 35.</p>'
             '<p>Labour law applies its own test. Section 200A of the Labour Relations Act presumes a person is '
             'an employee if any one of a list of indicators is present — such as working under your control or '
             'direction, or being economically dependent on you — for workers earning below the threshold set '
             'under the Basic Conditions of Employment Act.</p>'),
            ('What a contractor invoice should contain',
             '<ul>'
             '<li>The contractor’s full name or business name, address and contact details.</li>'
             '<li>An invoice number and date.</li>'
             '<li>Your business name as the client.</li>'
             '<li>A description of the work, the period, and the hours or deliverables it covers.</li>'
             '<li>The amount due and payment terms.</li>'
             '<li>VAT only if the contractor is a registered vendor — in which case it must meet the full '
             '<a href="/guides/vat-tax-invoice-requirements">tax invoice requirements</a>, including the '
             'contractor’s VAT number.</li>'
             '</ul>'),
            ('Contractors and VAT',
             '<p>A contractor who is not registered for VAT must not add VAT to an invoice. Registration becomes '
             'compulsory when taxable supplies exceed, or are expected to exceed, <strong>R2.3 million</strong> in '
             '12 months (from 1 April 2026; previously R1 million). Voluntary registration is possible from '
             'R120 000. If a contractor charges VAT, check their VAT number before you claim the input tax.</p>'),
            ('A clean contractor workflow',
             '<ol class="steps">'
             '<li><strong>Onboard</strong>: signed agreement, ID or company registration, tax number, VAT status '
             'and bank confirmation letter.</li>'
             '<li><strong>Record work</strong>: timesheets or deliverables against a client, site or project.</li>'
             '<li><strong>Invoice</strong>: the contractor submits an invoice that matches the approved work.</li>'
             '<li><strong>Approve</strong>: someone other than the person who captured the work approves it.</li>'
             '<li><strong>Pay</strong>: to the verified bank account only. Treat any request to change banking '
             'details as suspected fraud until confirmed by phone on a known number.</li>'
             '<li><strong>Keep the trail</strong>: agreement, timesheets, invoice, approval and proof of payment '
             'together, for at least five years.</li>'
             '</ol>'),
        ],
        'faqs': [
            ('Do I have to deduct PAYE from a contractor?',
             'Not from a genuine independent contractor. But if you control and supervise how the work is done, '
             'or the contractor is a personal service provider, SARS may treat the payment as remuneration and '
             'expect PAYE to have been withheld.'),
            ('Can a contractor charge VAT?',
             'Only if they are a registered VAT vendor. Registration is compulsory above R2.3 million of taxable '
             'supplies in 12 months from 1 April 2026, and voluntary from R120 000.'),
            ('What is a personal service provider?',
             'A company or trust through which a connected person personally provides employee-like services to '
             'a client. Payments to it can be subject to PAYE, and its deductions are restricted.'),
        ],
        'sources': [
            ('SARS — Pay As You Earn (PAYE)', 'https://www.sars.gov.za/types-of-tax/pay-as-you-earn/'),
            ('SARS — Value-Added Tax', 'https://www.sars.gov.za/types-of-tax/value-added-tax/'),
        ],
        'product': ('DivineBilling’s contractor portal is free for unlimited contractors on every plan: they '
                    'keep their profile, bank details and documents up to date, log timesheets and submit '
                    'invoices, and you approve them from one queue — with every admin change to an invoice '
                    'logged for year-end review.'),
    },
    {
        'slug': 'psira-security-company-operations',
        'title': 'Running a PSIRA-registered security company: guards, sites, the OB and billing',
        'seo_title': 'Running a PSIRA security company: ops & billing',
        'meta': ('A practical guide for South African security companies: PSIRA registration of the business and '
                 'every officer, grades A–E, the occurrence book, rosters, and invoicing per site.'),
        'summary': 'PSIRA compliance and daily operations for SA guarding companies, from grades to per-site invoices.',
        'dept': 'security',
        'published': '2026-10-09',
        'reviewed': REVIEWED,
        'takeaways': [
            'The Private Security Industry Regulation Authority (PSIRA) regulates private security under the Private Security Industry Regulation Act 56 of 2001.',
            'A security business must be registered with PSIRA before it renders security services, and so must every security officer it deploys.',
            'Security officers are graded from E (entry level) to A (highest), based on accredited training; the grade limits the duties an officer may perform.',
            'Directors and members of a security business must themselves be trained and registered with PSIRA.',
            'Registration must be kept current: lapsed officer or business registrations are a compliance failure that clients and PSIRA inspectors check.',
            'Minimum wages and conditions for guards are set specifically for the private security sector, so payroll must follow the sector rules, not general minimums.',
        ],
        'sections': [
            ('Who regulates private security in South Africa',
             '<p>The <strong>Private Security Industry Regulation Authority (PSIRA)</strong> was established by the '
             'Private Security Industry Regulation Act 56 of 2001. It registers security service providers, '
             'sets training standards, inspects businesses and enforces the code of conduct for the industry.</p>'),
            ('Registering the business',
             '<p>A company may not render security services — or tender for guarding contracts — until it is '
             'registered with PSIRA. Applications typically require:</p>'
             '<ul>'
             '<li>CIPC company registration documents.</li>'
             '<li>Proof of tax compliance and registration numbers for PAYE, UIF and COIDA (and VAT if registered).</li>'
             '<li>Every director, member or partner trained at an accredited institution and registered with PSIRA.</li>'
             '<li>A business plan and suitable fixed office premises, which PSIRA inspects.</li>'
             '</ul>'
             '<p>Registration carries annual fees and must be renewed. Fees change, so confirm the current schedule '
             'with PSIRA before you budget.</p>'),
            ('Registering and grading officers',
             '<p>Every security officer must be individually registered with PSIRA. Officers are graded on the '
             'accredited training they have completed:</p>'
             '<ul>'
             '<li><strong>Grade E</strong> — entry level, basic guarding.</li>'
             '<li><strong>Grades D and C</strong> — intermediate grades with more responsibility than entry-level '
             'guarding.</li>'
             '<li><strong>Grades B and A</strong> — supervisory and management roles, up to site commanders who '
             'run a workforce and assess risk.</li>'
             '</ul>'
             '<p>Deploy officers only to posts their grade allows. Keep a copy of each officer’s PSIRA certificate '
             'and track its expiry date — an officer whose registration has lapsed should not be on a post.</p>'),
            ('Daily operations: posts, rosters and the occurrence book',
             '<ul>'
             '<li><strong>Post orders</strong> — written instructions for each post: patrol routes, access rules, '
             'escalation contacts.</li>'
             '<li><strong>Occurrence book (OB)</strong> — the chronological record of everything that happens on '
             'a site: shift changes, patrols, visitors, incidents. Entries should be timed, signed and never '
             'erased; corrections are new entries.</li>'
             '<li><strong>Incident reports</strong> — a fuller record for anything that may lead to a claim, an '
             'insurance matter or a criminal case.</li>'
             '<li><strong>Rosters</strong> — who is on which post on which shift, so hours worked, overtime, '
             'Sunday and public-holiday time feed payroll accurately.</li>'
             '<li><strong>K9 units</strong> — dog records, handler pairing, training and vet history, and which '
             'site each team is deployed to.</li>'
             '</ul>'),
            ('Payroll for guards',
             '<p>Minimum wages and conditions for security officers are set specifically for the private security '
             'sector, and include rules on shift lengths, overtime, night work, Sunday and public-holiday pay. '
             'Check the current sectoral determination or bargaining council agreement each year when rates '
             'change. Guards are employees, so PAYE, UIF and SDL apply as for any payroll — see '
             '<a href="/guides/emp201-paye-uif-sdl">the EMP201 guide</a>.</p>'),
            ('Billing clients per site',
             '<p>Most guarding contracts are priced per post or per officer-shift on each site. Invoice per site '
             'so clients with several properties can approve each one, include the VAT details a '
             '<a href="/guides/vat-tax-invoice-requirements">full tax invoice</a> needs, and reconcile billed '
             'shifts against the roster before invoices go out — unbilled extra shifts are one of the most '
             'common sources of lost margin.</p>'),
            ('Compliance checklist',
             '<ul>'
             '<li>Business PSIRA registration current, certificate on file.</li>'
             '<li>Every deployed officer registered, graded for the post, and not expired.</li>'
             '<li>Directors registered and trained.</li>'
             '<li>OB and incident records complete for every site.</li>'
             '<li>Payroll on current sector rates; EMP201 filed by the 7th.</li>'
             '<li>Invoices per site, reconciled to the roster.</li>'
             '</ul>'),
        ],
        'faqs': [
            ('Does a security company have to register with PSIRA?',
             'Yes. A business must be registered with PSIRA before it renders security services, and every '
             'security officer it deploys must be registered too.'),
            ('What are the PSIRA grades?',
             'Security officers are graded from E, the entry level, to A, the highest, according to the '
             'accredited training they have completed. The grade determines which duties an officer may perform.'),
            ('Do directors of a security company need PSIRA registration?',
             'Yes. Directors, members and partners of a security business must be trained at an accredited '
             'institution and registered with PSIRA.'),
        ],
        'sources': [
            ('PSIRA — Private Security Industry Regulatory Authority', 'https://www.psira.co.za/'),
            ('SARS — Pay As You Earn (PAYE)', 'https://www.sars.gov.za/types-of-tax/pay-as-you-earn/'),
        ],
        'product': ('DivineBilling’s Security department keeps post orders, a digital occurrence book, incidents, '
                    'access control and rosters per site, linked to HR files with PSIRA grade and expiry '
                    'tracking, the K9 department, Payroll, and per-site invoicing.'),
    },
]

GUIDES_BY_SLUG = {g['slug']: g for g in GUIDES}
