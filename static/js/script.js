const projects = JSON.parse(document.getElementById('project-data').textContent);
const projectsGrid = document.getElementById('allProjectsGrid');
const featuredProjectsGrid = document.getElementById('featuredProjectsGrid');
const recentProjectsGrid = document.getElementById('recentProjectsGrid');
const projectModal = document.getElementById('projectModal');
const sections = document.querySelectorAll('.section');
const navItems = document.querySelectorAll('.nav-links a');
const pagination = document.getElementById('pagination');
let currentCategory = 'all';
let currentSearch = '';
let currentSort = 'date-desc';
let currentPage = 1;
const projectsPerPage = 6;

document.addEventListener('DOMContentLoaded', () => { loadProjects(); setupEventListeners(); });

function formatCategory(category) {
    return category.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

function filteredProjects() {
    return projects.filter(project => {
        const categoryMatch = currentCategory === 'all' || project.category === currentCategory;
        const term = currentSearch.toLowerCase();
        const searchable = [project.title, project.description, project.category_name, ...project.tags, ...project.components.map(item => item.name)].join(' ').toLowerCase();
        return categoryMatch && (!term || searchable.includes(term));
    });
}

function sortedProjects(items) {
    return [...items].sort((a, b) => {
        if (currentSort === 'name-asc') return a.title.localeCompare(b.title);
        if (currentSort === 'name-desc') return b.title.localeCompare(a.title);
        const dates = [new Date(a.date || 0), new Date(b.date || 0)];
        return currentSort === 'date-asc' ? dates[0] - dates[1] : dates[1] - dates[0];
    });
}

function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.innerHTML = `<img src="${project.image}" alt="${project.title}" class="project-thumbnail"><div class="project-info"><h3>${project.title}</h3><span class="project-category">${project.category_name || formatCategory(project.category)}</span></div>`;
    card.addEventListener('click', () => openProjectModal(project));
    return card;
}

function renderGrid(element, items) {
    element.innerHTML = '';
    items.forEach(project => element.appendChild(createProjectCard(project)));
}

function loadProjects() {
    const filtered = sortedProjects(filteredProjects());
    const start = (currentPage - 1) * projectsPerPage;
    renderGrid(projectsGrid, filtered.slice(start, start + projectsPerPage));
    renderGrid(featuredProjectsGrid, projects.filter(project => project.featured).slice(0, 3));
    renderGrid(recentProjectsGrid, sortedProjects(projects).slice(0, 3));
    updatePagination(filtered.length);
}

function updatePagination(total) {
    pagination.innerHTML = '';
    const pages = Math.ceil(total / projectsPerPage);
    if (pages <= 1) return;
    for (let page = 1; page <= pages; page++) {
        const link = document.createElement('a');
        link.href = '#'; link.textContent = page;
        if (page === currentPage) link.classList.add('active');
        link.addEventListener('click', event => { event.preventDefault(); currentPage = page; loadProjects(); });
        pagination.appendChild(link);
    }
}

function openProjectModal(project) {
    document.getElementById('modalProjectTitle').textContent = project.title;
    document.getElementById('projectDescription').textContent = project.description;
    document.getElementById('projectCategory').textContent = project.category_name || formatCategory(project.category);
    document.getElementById('projectDate').textContent = project.date;
    document.getElementById('projectTags').textContent = project.tags.join(', ');
    const mainMedia = document.querySelector('#projectModal .main-media');
    mainMedia.innerHTML = project.video ? `<video src="${project.video}" controls></video>` : (project.image ? `<img src="${project.image}" alt="${project.title}" class="main-preview-image">` : '');
    const gallery = document.getElementById('thumbnailGallery'); gallery.innerHTML = '';
    project.images.forEach(item => {
        const wrapper = document.createElement('div'); wrapper.className = 'gallery-item';
        wrapper.innerHTML = `<img src="${item.url}" alt="${item.caption || project.title}"><div class="image-caption">${item.caption || ''}</div>`;
        wrapper.addEventListener('click', () => { mainMedia.innerHTML = `<img src="${item.url}" alt="${item.caption || project.title}" class="main-preview-image">`; });
        gallery.appendChild(wrapper);
    });
    const steps = document.getElementById('projectSteps'); steps.innerHTML = '';
    project.steps.forEach(step => { const li = document.createElement('li'); li.textContent = step.title ? `${step.title}: ${step.description}` : step.description; steps.appendChild(li); });
    const components = document.getElementById('projectComponents'); components.innerHTML = '';
    project.components.forEach(item => { const li = document.createElement('li'); li.textContent = [item.quantity, item.name, item.notes].filter(Boolean).join(' - '); components.appendChild(li); });
    document.getElementById('projectCodeLink').href = project.codeLink || '#';
    document.getElementById('projectVideoLink').href = project.videoLink || '#';
    projectModal.style.display = 'block'; document.body.style.overflow = 'hidden';
}

function closeModal() { projectModal.style.display = 'none'; document.body.style.overflow = 'auto'; }
function showSection(id) { sections.forEach(section => section.classList.toggle('active-section', section.id === id)); }

function setupEventListeners() {
    document.querySelector('.close-btn').addEventListener('click', closeModal);
    window.addEventListener('click', event => { if (event.target === projectModal) closeModal(); });
    document.querySelector('.hamburger').addEventListener('click', () => { document.querySelector('.hamburger').classList.toggle('active'); document.querySelector('.nav-links').classList.toggle('active'); });
    navItems.forEach(item => item.addEventListener('click', event => { event.preventDefault(); showSection(item.getAttribute('href').substring(1)); }));
    document.querySelectorAll('.category-list a').forEach(link => link.addEventListener('click', event => { event.preventDefault(); currentCategory = link.dataset.category; currentPage = 1; loadProjects(); showSection('projects'); }));
    document.querySelectorAll('[data-tag]').forEach(tag => tag.addEventListener('click', event => { event.preventDefault(); document.getElementById('searchInput').value = tag.dataset.tag; currentSearch = tag.dataset.tag; currentCategory = 'all'; currentPage = 1; loadProjects(); showSection('projects'); }));
    const search = () => { currentSearch = document.getElementById('searchInput').value.trim(); currentCategory = 'all'; currentPage = 1; loadProjects(); showSection('projects'); };
    document.getElementById('searchBtn').addEventListener('click', search);
    document.getElementById('searchInput').addEventListener('keypress', event => { if (event.key === 'Enter') { event.preventDefault(); search(); } });
    document.getElementById('sortSelect').addEventListener('change', event => { currentSort = event.target.value; currentPage = 1; loadProjects(); });
}
