import { http, HttpResponse } from 'msw'

const API_BASE_URL = 'http://localhost:8000'

export const handlers = [
  http.get(`${API_BASE_URL}/api/sections/`, () => {
    // Respond with a 200 status and an empty array.
    return HttpResponse.json([])
  }),

  // Mock for a sample GET request
  http.get('/api/message', () => {
    return HttpResponse.json({
      message: 'This is a mocked message',
    })
  }),
]
