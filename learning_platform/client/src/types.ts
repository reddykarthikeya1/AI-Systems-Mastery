export interface LessonItem {
  id: string;
  title: string;
  file_path: string;
  type: 'theory' | 'playground' | 'project' | 'quiz' | 'troubleshooting' | 'code' | 'powershell' | 'notebook' | 'shell' | 'challenge';
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
  has_problems?: boolean;
  quickstart_script?: string | null;
  word_count?: number;
  reading_minutes?: number;
  quiz_question_count?: number;
}

export interface CourseSummary {
  id: string;
  course_num: number;
  title: string;
  folder_name: string;
  category: string;
  difficulty: string;
  estimated_hours: number;
  reading_hours?: number;
  lab_hours?: number;
  total_words?: number;
  debug_lab_count?: number;
  module_count: number;
  description: string;
  depth_badge?: string;
  quickstart_script?: string | null;
}

export interface LastPosition {
  course_id: string;
  course_title?: string;
  module_id: string;
  module_title?: string;
  lesson_id?: string;
  lesson_title?: string;
  lesson_path?: string;
  updated_at: number;
}

export interface SrsCardReview {
  interval_days: number;
  repetition: number;
  ease_factor: number;
  next_review_epoch: number;
}

export interface MasteryGateStatus {
  quizPassed: boolean;
  labPassed: boolean;
  dsaPassed?: boolean;
  projectPassed?: boolean;
  cleared: boolean;
  cleared_at?: number;
}

export interface CustomSrsCard {
  id: string;
  category: string;
  question: string;
  answer: string;
  keyTakeaway: string;
  sourceLessonId?: string;
  createdAt: number;
}

export interface EngineeringRank {
  level: number;
  title: string;
  minXp: number;
  maxXp: number;
  badge: string;
}

export const ENGINEERING_RANKS: EngineeringRank[] = [
  { level: 1, title: 'Junior Systems Engineer', minXp: 0, maxXp: 500, badge: '🌱' },
  { level: 2, title: 'Systems Apprentice', minXp: 500, maxXp: 1500, badge: '⚡' },
  { level: 3, title: 'Core Infrastructure Engineer', minXp: 1500, maxXp: 3500, badge: '🏗️' },
  { level: 4, title: 'Distributed Systems Architect', minXp: 3500, maxXp: 7000, badge: '🌐' },
  { level: 5, title: 'GPU Kernel Hacker', minXp: 7000, maxXp: 12000, badge: '🚀' },
  { level: 6, title: 'Principal AI Systems Architect', minXp: 12000, maxXp: 25000, badge: '👑' },
];

export interface ProgressPayload {
  completed_lessons: string[];
  completed_modules: string[];
  current_course?: string | null;
  current_lesson?: string | null;
  last_position?: LastPosition | null;
  sound_enabled?: boolean;
  srs_card_reviews?: Record<string, SrsCardReview>;
  srs_custom_cards?: CustomSrsCard[];
  mastery_gates?: Record<string, MasteryGateStatus>;
  last_updated: number;
  theme: 'dark' | 'light';
  quiz_scores?: Record<string, any>;
  bookmarks?: string[];
  notes?: Record<string, string>;
  last_study_date?: string;
  study_streak_days?: number;
  solved_problems?: string[];
  earned_xp?: number;
  welcome_dismissed?: boolean;
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

export interface DsaTestCase {
  input: any;
  expected: any;
  hidden?: boolean;
}

export interface DsaProblem {
  id: string;
  module_num: number;
  title: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  pattern: string;
  time_complexity: string;
  space_complexity: string;
  description: string;
  starter_code: string;
  visible_testcases: DsaTestCase[];
  hidden_testcase_count: number;
  is_design?: boolean;
  target_class?: string;
  filename?: string;
}

export interface DsaTestCaseResult {
  case_index: number;
  is_hidden: boolean;
  input: any;
  expected: any;
  actual: any;
  passed: boolean;
}

export interface DsaRunResult {
  status: 'accepted' | 'wrong_answer' | 'runtime_error' | 'time_limit_exceeded' | 'error';
  all_passed: boolean;
  total_cases: number;
  passed_cases: number;
  duration_ms: number;
  results: DsaTestCaseResult[];
  explanation?: string;
  reference_solution?: string;
  error?: string;
}

export interface SqlResult {
  status: 'success' | 'error';
  columns: string[];
  rows: any[][];
  row_count: number;
  duration_ms: number;
  query_plan: string[];
  error?: string;
}

export interface FormatCodeResult {
  formatted: string;
  status: 'formatted' | 'normalized' | 'unchanged' | 'error';
}

export interface ModuleProblem {
  id: string;
  filename: string;
  title: string;
  description: string;
  code: string;
  starter_code: string;
  has_tests: boolean;
}

export interface ModuleProblemsResponse {
  has_problems: boolean;
  module_path: string;
  readme: string | null;
  problems: ModuleProblem[];
}

export interface ProblemRunResult {
  status: 'passed' | 'failed' | 'timeout' | 'error';
  exit_code: number;
  stdout: string;
  stderr: string;
  duration_ms: number;
}
