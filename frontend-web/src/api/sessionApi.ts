import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export async function listSessions(): Promise<string[]> {
  const { data } = await client.get<{ sessions: string[] }>('/sessions')
  return data.sessions
}

export async function deleteSession(sessionId: string): Promise<void> {
  await client.delete(`/sessions/${sessionId}`)
}
