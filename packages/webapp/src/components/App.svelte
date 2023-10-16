<script>
  import IoMdSend from 'svelte-icons/io/IoMdSend.svelte';
  const API_BASE = '/api/chat';

  let formEl = null;
  let currQuestion = '';
  let thread = [];
  let answer = null;
  let loading = false;

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
    }
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

      let thread = [
        ...thread,
        { 
          type: 'answer',
          text: `${data.answer} ${data?.sources || 'no sources for this data'}`
        }
      ]
    } catch (err) {
      console.log('error', err);
      thread = [...thread, { 
        type: 'error',
        text: `something went wrong when asking your question: ${err}`
      }]
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
      {#each thread as {type, text}, i}
        <div class={`chat-message ${type}`}>
          {text}
        </div>
      {/each}
    </div>
    {#if loading}
      <p>loading...</p>
    {/if}
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

  :global(*) {
    box-sizing: border-box;
    font-family: sans-serif;
  }

  :global(html, body) {
    padding: 0;
    margin: 0;
    background: var(--gray-2);
  }

  .site-container {
    height: 100vh;
    display: grid;
    grid-template-rows: auto 1fr auto;
  }

  nav {
    border-bottom: 1px solid var(--gray-4);
    padding: var(--size-1) var(--size-2);
    display: grid;
    place-items: center;
    background: var(--gray-1);
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
      grid-template-columns: 1fr 1fr 1fr;
      width: 100%;
      max-width: 800px;
      gap: var(--size-3);
    }
  }

  div.chat-message {
    position: relative;
    grid-column: 2/4;
    padding: var(--size-2) var(--size-3);
    background: white;
    border-radius: var(--radius-round);

    & p {
      margin: 0px;
      font-size: var(--font-size-3);
      line-height: 1.5;
    }

    &.question {
      background: var(--gradient-17);
      color: white;
      border-bottom-right-radius: 0px;
      &:after {
        content: "";
        position: absolute;
        bottom: 0em;
        right: -1em;
        width: 1em;
        height: 1em;
        border-bottom-right-radius: 8rem;
        background: radial-gradient(circle at top right,rgba(0,0,0,0) 0,rgba(0,0,0,0) 1em,blue 1em);
      }
    }

    &:is(.answer, .error) {
      grid-column: 1/3;
      border-bottom-left-radius: 0px;
      &:after {
        content: "";
        position: absolute;
        bottom: 0em;
        left: -1em;
        width: 1em;
        height: 1em;
        border-bottom-left-radius: 8rem;
        background: radial-gradient(circle at top left,rgba(0,0,0,0) 0,rgba(0,0,0,0) 1em,white 1em);
      }
    }

    &.error {
      background: var(--red-8);
      color: var(--red-0);
      &:after {
        background: radial-gradient(circle at top left,rgba(0,0,0,0) 0,rgba(0,0,0,0) 1em,var(--red-8) 1em);
      }
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
    border: 1px solid var(--gray-3);
    border-radius: calc(var(--radius-2) + var(--radius-2));
    padding: var(--size-2);
    max-width: 800px;
    width: 100%;
    background: white;
    box-shadow: var(--shadow-2);
    &:focus-within {
      border-color: var(--blue-3);
      outline: 2px solid var(--blue-4);
      outline-offset: 3px;
    }
  }

  :global(input, select, textarea) {
    padding: var(--size-2);
    font-size: var(--font-size-2);
    border: none;
    resize: none;
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
      filter: grayscale(1) opacity(0.2);
    }
  }
</style>
