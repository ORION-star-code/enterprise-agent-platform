export interface ChatRequest {
  message: string
  session_id: string
}

export interface SourceItem {
  doc_name: string
  section: string
  score: number
}

export interface ChatResponse {
  response: string
  session_id: string
  intent: string | null
  sources: SourceItem[]
}

export interface TraceStep {
  node: string
  action: string
  details: Record<string, unknown>
}

export interface WorkflowTrace {
  trace_id: string
  session_id: string
  steps: TraceStep[]
  final_response: string | null
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  sources?: SourceItem[]
  intent?: string | null
  trace_id?: string
}
