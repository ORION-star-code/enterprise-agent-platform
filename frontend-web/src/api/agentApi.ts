import axios from 'axios'
import type { ChatRequest, ChatResponse, WorkflowTrace } from '@/types'

const client = axios.create({
  baseURL: '',
  timeout: 30000,
})

export async function sendMessage(req: ChatRequest): Promise<ChatResponse> {
  const { data } = await client.post<ChatResponse>('/chat', req)
  return data
}

export async function healthCheck(): Promise<{ status: string }> {
  const { data } = await client.get<{ status: string }>('/health')
  return data
}

export async function getTrace(traceId: string): Promise<WorkflowTrace> {
  const { data } = await client.get<WorkflowTrace>(`/api/traces/${traceId}`)
  return data
}
