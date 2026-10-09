"""Public SEO layer: robots, sitemap, llms.txt, /faq, canonical + JSON-LD."""
import json
import re

import pytest

import demo_mode

WWW = 'https://www.divinebilling.online'


@pytest.fixture()
def marketing(client, monkeypatch):
    """Render marketing pages as www would (the test env is otherwise a demo instance)."""
    monkeypatch.setattr(demo_mode, 'is_demo_site', lambda: False)
    return client


def _jsonld(html):
    return [json.loads(m) for m in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


def test_robots_points_at_www_sitemap_and_welcomes_ai_crawlers(client):
    body = client.get('/robots.txt').get_data(as_text=True)
    assert 'Sitemap: {}/sitemap.xml'.format(WWW) in body
    assert 'bill-all' not in body
    for bot in ('GPTBot', 'OAI-SearchBot', 'PerplexityBot', 'ClaudeBot', 'Google-Extended'):
        assert 'User-agent: {}'.format(bot) in body
    # Named groups must repeat the private-path rules, not just "*".
    assert body.count('Disallow: /admin') == 2


def test_sitemap_lists_www_urls_only(client):
    body = client.get('/sitemap.xml').get_data(as_text=True)
    locs = re.findall(r'<loc>(.*?)</loc>', body)
    assert WWW + '/' in locs
    assert WWW + '/faq' in locs
    assert WWW + '/solutions/security' in locs
    assert WWW + '/for-bookkeepers' in locs
    assert all(loc.startswith(WWW) for loc in locs)
    assert WWW + '/login' not in locs
    assert '<lastmod>' in body


def test_llms_txt_states_entity_and_live_prices(client):
    from modules_data import format_zar, get_pricing_tiers
    resp = client.get('/llms.txt')
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert body.startswith('# DivineBilling')
    assert 'not a medical billing service' in body
    assert 'Divine Online Solutions' in body
    basic = next(t for t in get_pricing_tiers() if t['id'] == 'basic')
    assert format_zar(basic['monthly']) in body
    assert '<a ' not in body


def test_faq_page_has_faqpage_schema_and_canonical(marketing):
    resp = marketing.get('/faq')
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert '<link rel="canonical" href="{}/faq">'.format(WWW) in html
    types = [d.get('@type') for d in _jsonld(html)]
    assert 'FAQPage' in types and 'BreadcrumbList' in types
    faq = next(d for d in _jsonld(html) if d.get('@type') == 'FAQPage')
    names = [q['name'] for q in faq['mainEntity']]
    assert 'Is DivineBilling a medical billing company?' in names
    assert all('<' not in q['acceptedAnswer']['text'] for q in faq['mainEntity'])


def test_marketing_pages_carry_site_graph(marketing):
    html = marketing.get('/pricing').get_data(as_text=True)
    graph = next(d for d in _jsonld(html) if '@graph' in d)['@graph']
    soft = next(n for n in graph if n['@type'] == 'SoftwareApplication')
    assert soft['offers']['priceCurrency'] == 'ZAR'
    assert 'medical' in soft['disambiguatingDescription']
    assert '<meta property="og:url" content="{}/pricing">'.format(WWW) in html


def test_apex_redirects_to_www(client):
    resp = client.get('/pricing?x=1', base_url='https://divinebilling.online')
    assert resp.status_code == 301
    assert resp.headers['Location'] == WWW + '/pricing?x=1'


def test_guides_index_and_articles_render_with_schema(marketing):
    from guides_content import GUIDES
    index = marketing.get('/guides').get_data(as_text=True)
    for g in GUIDES:
        assert '/guides/' + g['slug'] in index
        html = marketing.get('/guides/' + g['slug']).get_data(as_text=True)
        assert '<link rel="canonical" href="{}/guides/{}">'.format(WWW, g['slug']) in html
        types = [d.get('@type') for d in _jsonld(html)]
        assert {'Article', 'FAQPage', 'BreadcrumbList'} <= set(types)
        article = next(d for d in _jsonld(html) if d.get('@type') == 'Article')
        assert article['dateModified'] == g['reviewed']


def test_unknown_guide_is_404(marketing):
    assert marketing.get('/guides/not-a-guide').status_code == 404


def test_guides_in_sitemap_and_llms(client):
    from guides_content import GUIDES
    sitemap = client.get('/sitemap.xml').get_data(as_text=True)
    llms = client.get('/llms.txt').get_data(as_text=True)
    for g in GUIDES:
        assert '{}/guides/{}'.format(WWW, g['slug']) in sitemap
        assert g['title'] in llms


def test_vat_guide_uses_2026_threshold():
    from guides_content import GUIDES_BY_SLUG
    text = str(GUIDES_BY_SLUG['vat-tax-invoice-requirements'])
    assert 'R2.3 million' in text and 'R120 000' in text
