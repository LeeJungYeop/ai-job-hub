const jobList = document.getElementById("job-list");
const emptyState = document.getElementById("empty-state");
const searchInput = document.getElementById("search-input");
const sourceFilter = document.getElementById("source-filter");
const keywordFilter = document.getElementById("keyword-filter");
const experienceFilter = document.getElementById("experience-filter");
const sortFilter = document.getElementById("sort-filter");
const countEl = document.getElementById("count");
const updatedEl = document.getElementById("updated");

let allJobs = [];

boot();

async function boot() {
  try {
    const res = await fetch("./jobs.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    allJobs = Array.isArray(data.jobs) ? data.jobs : [];

    updatedEl.textContent = `업데이트: ${data.updated_at}`;

    initFilters();
    bindEvents();
    render();
  } catch (err) {
    emptyState.hidden = false;
    emptyState.textContent = "데이터를 불러오지 못했습니다.";
    console.error(err);
  }
}

function initFilters() {
  const sources = [...new Set(allJobs.map(j => j.source).filter(Boolean))].sort();
  sources.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s;
    opt.textContent = s;
    sourceFilter.append(opt);
  });

  const keywords = [...new Set(allJobs.map(j => j.keyword).filter(Boolean))].sort();
  keywords.forEach(k => {
    const opt = document.createElement("option");
    opt.value = k;
    opt.textContent = k;
    keywordFilter.append(opt);
  });
}

function bindEvents() {
  searchInput.addEventListener("input", render);
  sourceFilter.addEventListener("change", render);
  keywordFilter.addEventListener("change", render);
  experienceFilter.addEventListener("change", render);
  sortFilter.addEventListener("change", render);
}

function render() {
  const search = searchInput.value.trim().toLowerCase();
  const source = sourceFilter.value;
  const keyword = keywordFilter.value;
  const experience = experienceFilter.value;
  const sort = sortFilter.value;

  let filtered = allJobs.filter(job => {
    if (source !== "all" && job.source !== source) return false;
    if (keyword !== "all" && job.keyword !== keyword) return false;
    if (experience !== "all") {
      const exp = job.experience || "";
      if (experience === "신입" && !exp.includes("신입")) return false;
      if (experience === "경력무관" && !exp.includes("경력무관")) return false;
      if (experience === "경력" && (exp.includes("신입") || exp.includes("경력무관") || !exp)) return false;
    }
    if (search) {
      const hay = [job.title, job.company, job.location].join(" ").toLowerCase();
      if (!hay.includes(search)) return false;
    }
    return true;
  });

  if (sort === "company") {
    filtered.sort((a, b) => (a.company || "").localeCompare(b.company || "", "ko"));
  }

  countEl.textContent = `${filtered.length}개`;
  jobList.replaceChildren(...filtered.map((job, i) => renderItem(job, i + 1)));
  emptyState.hidden = filtered.length > 0;
}

function renderItem(job, rank) {
  const item = document.createElement("li");
  item.className = "job-item";

  const rankEl = document.createElement("div");
  rankEl.className = "job-rank";
  rankEl.textContent = `${String(rank).padStart(2, "0")}.`;

  const body = document.createElement("article");
  body.className = "job-main";

  // 제목 행
  const titleRow = document.createElement("div");
  titleRow.className = "job-title-row";

  const titleLeft = document.createElement("div");
  titleLeft.className = "job-title-left";

  const titleLink = document.createElement("a");
  titleLink.className = "job-title";
  titleLink.href = job.url;
  titleLink.target = "_blank";
  titleLink.rel = "noreferrer";
  titleLink.textContent = job.title;
  titleLeft.append(titleLink);
  titleRow.append(titleLeft);

  // 메타 행
  const meta = document.createElement("div");
  meta.className = "job-submeta";

  const sourceSpan = document.createElement("span");
  sourceSpan.className = `job-source source-${job.source || "default"}`;
  sourceSpan.textContent = job.source;
  meta.append(sourceSpan);

  if (job.company) {
    meta.append(subSpan(job.company));
  }

  if (job.location) {
    meta.append(subSpan(job.location));
  }

  if (job.experience) {
    meta.append(subSpan(job.experience));
  }

  if (job.company_size) {
    meta.append(subSpan(job.company_size));
  }

  if (job.keyword) {
    const tag = document.createElement("div");
    tag.className = "job-tag";
    tag.textContent = job.keyword;
    meta.append(tag);
  }

  body.append(titleRow, meta);
  item.append(rankEl, body);
  return item;
}

function subSpan(text) {
  const span = document.createElement("span");
  span.textContent = text;
  return span;
}
