import {
  CourseSummary,
  ModuleItem,
  ProgressPayload,
  TestResult,
  RunnerMode,
  DsaProblem,
  DsaRunResult,
  SqlResult,
  FormatCodeResult,
} from '../types';

const API_BASE = '/api';

export async function fetchCourses(): Promise<CourseSummary[]> {
  const res = await fetch(`${API_BASE}/courses`);
  if (!res.ok) throw new Error('Failed to load courses');
  return res.json();
}

export async function fetchCourseModules(courseId: string): Promise<ModuleItem[]> {
  const res = await fetch(`${API_BASE}/courses/${encodeURIComponent(courseId)}/modules`);
  if (!res.ok) throw new Error('Failed to load course modules');
  return res.json();
}

export async function fetchModuleQuiz(modulePath: string): Promise<any[]> {
  try {
    const res = await fetch(`${API_BASE}/quiz?module_path=${encodeURIComponent(modulePath)}`);
    if (res.ok) return res.json();
  } catch (e) {
    console.warn('Could not fetch structured quiz from server', e);
  }
  return [];
}

export async function fetchFileContent(path: string): Promise<{ content: string; filename: string; extension: string }> {
  const res = await fetch(`${API_BASE}/content?path=${encodeURIComponent(path)}`);
  if (!res.ok) throw new Error('Failed to load file');
  return res.json();
}

export async function runTestCommand(targetPath: string, commandType: 'pytest' | 'python' = 'pytest'): Promise<TestResult> {
  const res = await fetch(`${API_BASE}/run-test`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ target_path: targetPath, command_type: commandType }),
  });
  if (!res.ok) throw new Error('Test execution failed to dispatch');
  return res.json();
}

export async function runInteractiveCode(
  code: string,
  mode: RunnerMode = 'python',
  workingDir?: string,
  timeoutSec: number = 25
): Promise<TestResult> {
  const res = await fetch(`${API_BASE}/run-code`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code,
      mode,
      working_dir: workingDir,
      timeout_sec: timeoutSec,
    }),
  });
  if (!res.ok) throw new Error('Code execution failed to dispatch');
  return res.json();
}

export async function fetchProgress(): Promise<ProgressPayload> {
  try {
    const res = await fetch(`${API_BASE}/progress`);
    if (res.ok) return res.json();
  } catch (e) {
    console.warn('Could not sync with backend progress endpoint, relying on localStorage', e);
  }
  return {
    completed_lessons: [],
    completed_modules: [],
    last_updated: Date.now(),
    theme: 'dark',
  };
}

export async function saveProgress(payload: ProgressPayload): Promise<void> {
  try {
    await fetch(`${API_BASE}/progress`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    console.warn('Failed to persist progress to disk', e);
  }
}

export async function fetchDsaProblems(module?: string): Promise<DsaProblem[]> {
  const url = module ? `${API_BASE}/dsa-problems?module=${encodeURIComponent(module)}` : `${API_BASE}/dsa-problems`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to load DSA problems');
  return res.json();
}

export async function runDsaTest(problemId: string, code: string, submit: boolean = false): Promise<DsaRunResult> {
  const res = await fetch(`${API_BASE}/run-dsa-test`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      problem_id: problemId,
      code,
      submit,
    }),
  });
  if (!res.ok) throw new Error('DSA test execution failed to dispatch');
  return res.json();
}

export async function formatCode(code: string, language: string = 'python'): Promise<FormatCodeResult> {
  const res = await fetch(`${API_BASE}/format-code`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, language }),
  });
  if (!res.ok) throw new Error('Code formatting failed');
  return res.json();
}

export async function executeSql(query: string, schemaPreset: string = 'storage_engine'): Promise<SqlResult> {
  const res = await fetch(`${API_BASE}/execute-sql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, schema_preset: schemaPreset }),
  });
  if (!res.ok) throw new Error('SQL execution failed');
  return res.json();
}

export async function fetchModuleTrace(modulePath: string): Promise<any | null> {
  try {
    const res = await fetch(`${API_BASE}/trace?module_path=${encodeURIComponent(modulePath)}`);
    if (res.ok) return res.json();
  } catch (e) {
    console.warn('Could not fetch module trace', e);
  }
  return null;
}

