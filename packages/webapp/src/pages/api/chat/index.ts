// this proxies the chat API to the backend
// I don't want to expose this directly incase I want to partially shut it down
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ url }) => {
  // parse the q query param
  const q = new URL(url).searchParams.get('q');
  if(!q) {
    return new Response('no question was provided (q).', { status: 400 });
  }

  // TODO: add a check here to make sure that I'm not above my OpenAPI budget 

  // fetch the response from the backend
  const API_URL = import.meta.env.CHAT_API_URL;
  const res = await fetch(`${API_URL}/api/chat?q=${q}`);
  const data = await res.json();

  // TODO: add a check here to add a warning if the answer doesn't have a source

  return new Response(JSON.stringify(data), {
    headers: {
      'content-type': 'application/json'
    }
  })

};