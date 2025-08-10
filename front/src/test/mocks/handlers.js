import { http, HttpResponse } from 'msw'

export const handlers = [
  // Mock for a sample GET request
  http.get('/api/message', () => {
    return HttpResponse.json({
      message: 'This is a mocked message',
    })
  }),
]
