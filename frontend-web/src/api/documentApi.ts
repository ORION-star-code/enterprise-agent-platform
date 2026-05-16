import axios from 'axios'

interface UploadResult {
  doc_id: string
  filename: string
  chunk_count: number
}

interface CollectionStatus {
  collection: string
  chunk_count: number
}

const client = axios.create({
  baseURL: '/api/rag',
  timeout: 60000,
})

export async function uploadDocument(file: File): Promise<UploadResult> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await client.post<UploadResult>('/documents/upload', form)
  return data
}

export async function getCollectionStatus(): Promise<CollectionStatus> {
  const { data } = await client.get<CollectionStatus>('/collection/status')
  return data
}
