<script>
  import IoMdSend from 'svelte-icons/io/IoMdSend.svelte';
  import { newMessageStream, thread, threadLoading } from '../../utils/stores';

  import { onDestroy } from 'svelte';

  let formEl = null;
  let currQuestion = '';
  let threadId;

  const API_BASE = '/api/chat';

  const unsubThread = thread.subscribe((value) => {
    // if there are messages in the thread on change, scroll the newest message into view
    if (value.length > 0) {
      setTimeout(() => {
        let chatMessageEls = document.querySelectorAll('.chat-message');
        let newChatEl = chatMessageEls[chatMessageEls.length - 1];
        newChatEl.scrollIntoView({ behavior: 'smooth' });
      }, 10);
    }
  });
  onDestroy(unsubThread);

  const handleEnterKey = (e) => {
    if (e.key == 'Enter' && !e.shiftKey) {
      e.preventDefault();
      formEl.dispatchEvent(new Event('submit'));
    }
  };

  const submitQuestionForm = async (e) => {
    e.preventDefault();
    threadLoading.set(true);
    newMessageStream.set(''); // clear the new message stream

    // optional analytics
    if (umami) {
      umami.track('Question asked');
    }

    const newQuestion = {
      type: 'question',
      text: currQuestion,
    };
    thread.update((t) => [...t, newQuestion]);
    currQuestion = '';

    try {
      // get data from form as object
      const form = new FormData(e.target);
      const formData = Object.fromEntries(form.entries());

      // construct URL params
      const params = new URLSearchParams(formData);

      // call the API
      const res = await fetch(`${API_BASE}?${params.toString()}`);
      if (res.status !== 200) throw new Error(res.statusText);

      // set the threadId 
      threadId = res.headers.get('lb-thread-id');

      // streaming
      const reader = res.body.getReader();
      const decoder = new TextDecoder('utf-8');

      let message = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }
        const chunk = decoder.decode(value);
        const dataPortions = chunk.split('data:');
        for(let i = 0; i < dataPortions.length; i++){
          const parseable = dataPortions[i];
          if (parseable.includes('[DONE]')){
            break;
          }
          if (parseable.trim() === '' || parseable.length <= 1) {
            continue;
          }
          const data = JSON.parse(parseable);
          if (data.choices[0].delta.content) {
            message += data.choices[0].delta.content;
            newMessageStream.update((m) => m + data.choices[0].delta.content);
          }
        }
      }

      const newResponseMessage = {
        type: 'answer',
        text: message,
        sources: 'tbd',
      };

      thread.update((t) => [...t, newResponseMessage]);

      if (umami) {
        umami.track('Question answered');
      }
    } catch (err) {
      const errChatMessage = {
        type: 'error',
        text: `something went wrong when asking your question: ${err}`,
      };
      thread.update((t) => [...t, errChatMessage]);
      if (umami) {
        umami.track('Question error');
      }
    }
    currQuestion = '';
    threadLoading.set(false);
  };
</script>

<section class="chatform">
  <form
    bind:this={formEl}
    on:submit={submitQuestionForm}
    method="GET"
    target="https://chat-api-production-cb57.up.railway.app/api/chat/"
  >
    <textarea
      on:keydown={handleEnterKey}
      id="q"
      name="q"
      placeholder="what do you think about docker?"
      bind:value={currQuestion}
    />
    <input 
      type="hidden" 
      name="threadId" 
      bind:value={threadId} 
    />
    <button
      class="icon"
      type="submit"
      aria-label="Ask question"
      title="Ask question"
      disabled={currQuestion.length <= 0 || $threadLoading}
    >
      <IoMdSend />
    </button>
  </form>
</section>

<style>
  section.chatform {
    position: sticky;
    bottom: var(--size-3);
    padding: var(--size-3);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  form {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: var(--size-4);
    border: 1px solid var(--paper-4);
    border-radius: calc(var(--radius-2) + var(--radius-2));
    padding: var(--size-2);
    max-width: 800px;
    width: 100%;
    background: var(--paper-1);
    box-shadow: var(--shadow-2);
    &:focus-within {
      border-color: var(--blue-3);
      outline: 2px solid var(--blue-4);
      outline-offset: 3px;
    }
  }

  button.icon {
    width: 40px;
    height: 40px;
    padding: var(--size-2);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-round);
    background: var(--gradient-17);
    border: none;
    color: white;
    transition: all 0.3s var(--ease-out-2);
    &:disabled {
      filter: grayscale(1) opacity(0.3);
    }
  }

  textarea {
    min-height: 4rem;
  }
</style>
