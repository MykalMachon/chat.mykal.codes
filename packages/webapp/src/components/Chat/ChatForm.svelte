<script>
  import IoMdSend from 'svelte-icons/io/IoMdSend.svelte';
  import { thread, threadLoading } from '../../utils/stores';

  import { onDestroy } from 'svelte';

  let formEl = null;
  let currQuestion = '';

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
      const data = await res.json();

      if (res.status !== 200) throw new Error(data.message);

      const newResponseMessage = {
        type: 'answer',
        text: `${data.answer} ${data?.sources || 'no sources for this data'}`,
      };

      thread.update((t) => [...t, newResponseMessage]);
    } catch (err) {
      console.log('error', err);
      const errChatMessage = {
        type: 'error',
        text: `something went wrong when asking your question: ${err}`,
      };
      thread.update((t) => [...t, errChatMessage]);
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
