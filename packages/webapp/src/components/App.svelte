<script>
  import IoMdSend from 'svelte-icons/io/IoMdSend.svelte';
  import { fly } from 'svelte/transition';
  const API_BASE = '/api/chat';

  let formEl = null;
  let currQuestion = '';
  let thread = [];
  let loading = false;

  // TODO: there's probably a better way to do this...
  $: if (thread.length > 0) {
    setTimeout(() => {
      let chatMessageEls = document.querySelectorAll('.chat-message');
      let newChatEl = chatMessageEls[chatMessageEls.length - 1];
      newChatEl.scrollIntoView({ behavior: 'smooth' });
    }, 10);
  }

  const handleEnterKey = (e) => {
    if (e.key == 'Enter' && !e.shiftKey) {
      e.preventDefault();
      formEl.dispatchEvent(new Event('submit'));
    }
  };

  const submitQuestionForm = async (e) => {
    e.preventDefault();

    loading = true;

    const newQuestion = {
      type: 'question',
      text: currQuestion,
    };
    thread = [...thread, newQuestion];

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

      thread = [
        ...thread,
        {
          type: 'answer',
          text: `${data.answer} ${data?.sources || 'no sources for this data'}`,
        },
      ];
    } catch (err) {
      console.log('error', err);
      thread = [
        ...thread,
        {
          type: 'error',
          text: `something went wrong when asking your question: ${err}`,
        },
      ];
    }
    currQuestion = '';
    loading = false;
  };
</script>

<div class="site-container">
  <nav>
    <h1>Mykal.ai</h1>
  </nav>

  <main>
    <div class="chat-message__container">
      {#each thread as { type, text }, i}
        <div in:fly={{ y: 12, duration: 450 }} class={`chat-message ${type}`}>
          <p>
            {text}
          </p>
        </div>
      {/each}
      {#if loading}
        <div in:fly={{ y: 12, duration: 450 }} class="chat-message answer">
          <p>Let me think about that...🤔</p>
        </div>
      {/if}
    </div>
  </main>

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
        disabled={currQuestion.length <= 0 || loading}
      >
        <IoMdSend />
      </button>
    </form>
  </section>
</div>

<style>
  @import 'https://unpkg.com/open-props';

  :global(:root) {
    --font-size-sm: clamp(0.8rem, 0.17vw + 0.76rem, 0.89rem);
    --font-size-base: clamp(1rem, 0.34vw + 0.91rem, 1.19rem);
    --font-size-md: clamp(1.25rem, 0.61vw + 1.1rem, 1.58rem);
    --font-size-lg: clamp(1.56rem, 1vw + 1.31rem, 2.11rem);
    --font-size-xl: clamp(1.95rem, 1.56vw + 1.56rem, 2.81rem);
    --font-size-xxl: clamp(2.44rem, 2.38vw + 1.85rem, 3.75rem);
    --font-size-xxxl: clamp(3.05rem, 3.54vw + 2.17rem, 5rem);

    --paper-1: var(--gray-0);
    --paper-2: var(--gray-1);
    --paper-3: var(--gray-2);
    --paper-4: var(--gray-4);

    --ink-1: var(--gray-12);
    --ink-2: var(--gray-10);
    --ink-3: var(--gray-9);
    --ink-4: var(--gray-8);
  }

  @media screen and (prefers-color-scheme: dark) {
    :global(:root) {
      --paper-1: var(--gray-12);
      --paper-2: var(--gray-11);
      --paper-3: var(--gray-10);
      --paper-4: var(--gray-9);

      --ink-1: var(--gray-0);
      --ink-2: var(--gray-1);
      --ink-3: var(--gray-3);
      --ink-4: var(--gray-4);
    }
  }

  :global(*) {
    box-sizing: border-box;
    font-family: sans-serif;
  }

  :global(html, body) {
    padding: 0;
    margin: 0;
    background: var(--paper-3);
    color: var(--ink-1);
  }

  .site-container {
    height: 100vh;
    display: grid;
    grid-template-rows: auto 1fr auto;
  }

  nav {
    border-bottom: 1px solid var(--paper-4);
    padding: var(--size-1) var(--size-2);
    display: grid;
    place-items: center;
    background: var(--paper-2);

    & h1 {
      font-size: var(--font-size-base);
      font-family: var(--font-mono);
      font-weight: bold;
      text-transform: uppercase;
      letter-spacing: var(--size-1);
    }
  }

  main {
    bottom: var(--size-3);
    padding: var(--size-3) var(--size-2);
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    & .chat-message__container {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
      width: 100%;
      max-width: 800px;
      gap: var(--size-3);
      padding: 0 var(--size-3);
    }
  }

  div.chat-message {
    position: relative;
    grid-column: 2/6;
    padding: var(--size-3);
    background: white;
    border-radius: var(--radius-3);

    & p {
      margin: 0px;
      font-size: var(--font-size-base);
      line-height: 1.5;
    }

    &.question {
      background: var(--gradient-17);
      color: white;
      border-bottom-right-radius: 0px;
      &:after {
        content: '';
        position: absolute;
        bottom: 0em;
        right: -1em;
        width: 1em;
        height: 1em;
        border-bottom-right-radius: 8rem;
        background: radial-gradient(
          circle at top right,
          rgba(0, 0, 0, 0) 0,
          rgba(0, 0, 0, 0) 1em,
          blue 1em
        );
      }
    }

    &:is(.answer, .error) {
      grid-column: 1/5;
      border-bottom-left-radius: 0px;
      background: var(--paper-4);
      color: var(--ink-1);
      &:after {
        content: '';
        position: absolute;
        bottom: 0em;
        left: -1em;
        width: 1em;
        height: 1em;
        border-bottom-left-radius: 8rem;
        background: radial-gradient(
          circle at top left,
          rgba(0, 0, 0, 0) 0,
          rgba(0, 0, 0, 0) 1em,
          var(--paper-4) 1em
        );
      }
    }

    &.error {
      background: var(--red-8);
      color: var(--red-0);
      &:after {
        background: radial-gradient(
          circle at top left,
          rgba(0, 0, 0, 0) 0,
          rgba(0, 0, 0, 0) 1em,
          var(--red-8) 1em
        );
      }
    }
  }

  @media screen and (max-width: 800px) {
    main div.chat-message__container {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }

    div.chat-message {
      width: 100%;
    }
  }

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

  :global(input, select, textarea) {
    padding: var(--size-2);
    font-size: var(--font-size-base);
    border: none;
    resize: none;
    background: var(--paper-1);
    color: var(--ink-1);
    &:focus {
      outline: none;
    }
  }

  :global(textarea) {
    min-height: 4rem;
  }
  :global(button.icon) {
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
</style>
