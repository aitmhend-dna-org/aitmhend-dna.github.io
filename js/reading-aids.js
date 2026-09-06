document.addEventListener('DOMContentLoaded', function () {
    const main = document.getElementById('main-content');
    if (!main) return;

    // A landing page's card titles are navigation, not article sections — a TOC
    // of them just repeats what is already on screen (#51).
    if (main.dataset.readingAids === 'off') return;

    const headings = Array.from(main.querySelectorAll('h2'));
    if (headings.length < 3) return;
    main.classList.add('has-reading-aids');

    function slugify(text) {
        return String(text || '')
            .toLowerCase()
            .normalize('NFKD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9\s-]/g, '')
            .trim()
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-');
    }

    function ensureHeadingIds(items) {
        const used = new Set();
        items.forEach(function (heading, idx) {
            let base = slugify(heading.textContent) || ('section-' + (idx + 1));
            let id = base;
            let n = 2;
            while (used.has(id) || document.getElementById(id)) {
                id = base + '-' + n;
                n += 1;
            }
            used.add(id);
            if (!heading.id) heading.id = id;
        });
    }

    ensureHeadingIds(headings);

    const progress = document.createElement('div');
    progress.className = 'reading-progress';
    progress.innerHTML = '<span class="reading-progress-bar" aria-hidden="true"></span>';
    document.body.appendChild(progress);
    const progressBar = progress.querySelector('.reading-progress-bar');

    const toc = document.createElement('section');
    toc.className = 'card toc-card';
    toc.setAttribute('aria-label', 'Table of contents');
    toc.innerHTML = [
        '<div class="toc-header">',
        '<h2 class="toc-title">On This Page</h2>',
        '<button type="button" class="toc-toggle" aria-expanded="true">Hide sections</button>',
        '</div>',
        '<ol class="toc-list"></ol>'
    ].join('');
    const tocList = toc.querySelector('.toc-list');
    const tocToggle = toc.querySelector('.toc-toggle');

    headings.forEach(function (heading) {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#' + heading.id;
        a.textContent = heading.textContent.trim();
        li.appendChild(a);
        tocList.appendChild(li);
    });

    const anchor = main.querySelector('.editorial-meta') || main.querySelector('.page-title');
    if (anchor && anchor.nextSibling) {
        main.insertBefore(toc, anchor.nextSibling);
    } else {
        main.insertBefore(toc, main.firstChild);
    }

    const backTop = document.createElement('button');
    backTop.className = 'back-to-top';
    backTop.type = 'button';
    backTop.setAttribute('aria-label', 'Back to top');
    backTop.textContent = 'Back to top';
    backTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    document.body.appendChild(backTop);

    const tocLinks = Array.from(toc.querySelectorAll('a'));
    const mainNav = document.querySelector('.main-nav');

    if (tocToggle) {
        tocToggle.addEventListener('click', function () {
            const isExpanded = tocToggle.getAttribute('aria-expanded') === 'true';
            toc.classList.toggle('is-collapsed', isExpanded);
            tocToggle.textContent = isExpanded ? 'Show sections' : 'Hide sections';
            tocToggle.setAttribute('aria-expanded', String(!isExpanded));
        });
    }

    function updateReadingAids() {
        const doc = document.documentElement;
        const scrollTop = window.scrollY || doc.scrollTop || 0;
        const max = Math.max(doc.scrollHeight - window.innerHeight, 1);
        const pct = Math.min(100, Math.max(0, (scrollTop / max) * 100));
        progressBar.style.width = pct + '%';

        const stickyTrigger = mainNav ? (mainNav.offsetTop + 8) : 90;
        progress.classList.toggle('is-visible', scrollTop > stickyTrigger);

        backTop.classList.toggle('is-visible', scrollTop > 520);

        let activeId = '';
        const threshold = scrollTop + 140;
        headings.forEach(function (heading) {
            if (heading.offsetTop <= threshold) {
                activeId = heading.id;
            }
        });

        tocLinks.forEach(function (link) {
            const isActive = link.getAttribute('href') === '#' + activeId;
            link.classList.toggle('is-active', isActive);
        });
    }

    window.addEventListener('scroll', updateReadingAids, { passive: true });
    window.addEventListener('resize', updateReadingAids);
    updateReadingAids();
});
