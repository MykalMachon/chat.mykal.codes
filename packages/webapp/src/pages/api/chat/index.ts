// this proxies the chat API to the backend
// I don't want to expose this directly incase I want to partially shut it down
import type { APIRoute } from 'astro';

type LangbaseDataType = {
  threadId?: string;
  messages: {
    role: string;
    content: string
  }[]
}

export const GET: APIRoute = async ({ url, request }) => {
  // parse the q query param
  const q = new URL(url).searchParams.get('q');
  if (!q) {
    return new Response('no question was provided (q).', { status: 400 });
  }

  // optional, thread id to keep track of the conversation
  const threadId = new URL(url).searchParams.get('threadId') || null;

  // TODO: add a check here to make sure that I'm not above my OpenAPI budget 

  const LANGBASE_URL = import.meta.env.LANGBASE_URL;
  const LANGBASE_API_KEY = import.meta.env.LANGBASE_API_KEY;

  if (!LANGBASE_URL || !LANGBASE_API_KEY) {
    return new Response('the api is improperly configured. See server logs.', { status: 500 });
  }

  // console.log(`q: ${q}`);
  // console.log(`threadId: ${threadId}`);

  try {
    const data: LangbaseDataType = {
      messages: [{ role: 'user', content: q }]
    }
    if (threadId) {
      data['threadId'] = threadId;
    }

    const response = await fetch(`${LANGBASE_URL}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${LANGBASE_API_KEY}`
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      console.error('failed to fetch from the chat API', response);
      return new Response('failed to fetch from the chat API. See server logs.', { status: 500 });
    }

    // stream response back to the client as it comes in
    const reader = response.body?.getReader();
    if (!reader) {
      return new Response('failed to fetch from the chat API. See server logs.', { status: 500 });
    }

    const body = new ReadableStream({
      // 
      async start(controller) {
        const decoder = new TextDecoder('utf-8');
        const encoder = new TextEncoder();

        const sendEvent = (data: string) => {
          controller.enqueue(encoder.encode(data));
        }

        request.signal.addEventListener('abort', () => {
          reader.cancel();
          controller.close();
        });

        let buffer = '';
        while(true) {
          const { done, value } = await reader.read();
          if (done) {
            controller.close();
            break;
          }
          const chunk = decoder.decode(value);          
          if(chunk.startsWith('data:') || chunk.startsWith('[DONE]')) {
            sendEvent(buffer);
            buffer = chunk;
          } else {
            buffer += chunk;
          }
        }
      }
    });

    return new Response(body, {
      headers: {
        'lb-thread-id': response.headers.get('lb-thread-id') || '',
        'content-type': 'text/event-stream',
        'cache-control': 'no-cache',
        'connection': 'keep-alive'
      }
    })
  } catch (err) {
    console.error(err)
    return new Response('failed to fetch from the chat API. See server logs.', { status: 500 });
  }
};