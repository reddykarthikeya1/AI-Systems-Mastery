export interface LessonItem {
  id: string;
  title: string;
  file_path: string;
  type: 'theory' | 'playground' | 'project' | 'quiz' | 'troubleshooting' | 'code';
}

export interface ModuleItem {
  id: string;
  module_num: number;
  title: string;
  folder_path: string;
  lessons: LessonItem[];
  has_solution: boolean;
  has_starter: boolean;
  has_debug_lab?: boolean;
  quickstart_script?: string | null;
}

export interface CourseSummary {
  id: string;
  course_num: number;
  title: string;
  folder_name: string;
  category: string;
  difficulty: string;
  estimated_hours: number;
  module_count: number;
  description: string;
  quickstart_script?: string | null;
}

export interface ProgressPayload {
  completed_lessons: string[];
  completed_modules: string[];
  current_course?: string | null;
  current_lesson?: string | null;
  last_updated: number;
  theme: 'dark' | 'light';
  quiz_scores?: Record<string, number>;
  bookmarks?: string[];
  notes?: Record<string, string>;
  last_study_date?: string;
  study_streak_days?: number;
}

export type RunnerMode = 'python' | 'powershell' | 'shell';

export interface TestResult {
  exit_code: number;
  stdout: string;
  stderr: string;
  duration_sec: number;
  status: 'passed' | 'failed' | 'timeout' | 'error';
  cwd?: string;
  mode?: RunnerMode;
}

