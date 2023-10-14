<script>
  import IoMdSend from 'svelte-icons/io/IoMdSend.svelte';
  const API_BASE = '/api/chat';

  let formEl = null;
  let question = '';
  let answer = null;
  let loading = false;

  const handleEnterKey = (e) => {
    console.log(e.key);
    if (e.key == 'Enter' && !e.shiftKey) {
      e.preventDefault();
      console.log('submitting form');
      formEl.dispatchEvent(new Event('submit'));
    }
  };

  const submitQuestionForm = async (e) => {
    e.preventDefault();
		answer = null;
    loading = true;

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

      answer = data;
    } catch (err) {
      console.log('error', err);
      answer = { answer: err, sources: [] };
    }
    question = '';
    loading = false;
  };
</script>

<nav>
  <h1>Mykal.ai</h1>
</nav>

<main>
  {#if !answer}
    {#if loading}
      <p>loading...</p>
    {:else}
      <p>Ask a question!</p>
    {/if}
  {:else}
    <p>
      {answer.answer}
    </p>
    <p>
      {#if answer.sources}
        sources:
        {answer.sources}
      {/if}
    </p>
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
      bind:value={question}
    />
    <button
      class="icon"
      type="submit"
      disabled={question.length <= 0 || loading}
    >
      <IoMdSend />
    </button>
  </form>
</section>

<style>
  @import 'https://unpkg.com/open-props';

  :global(*) {
    box-sizing: border-box;
    font-family: sans-serif;
  }

  :global(html, body) {
    padding: 0;
    margin: 0;
  }

	main, nav {
    bottom: var(--size-3);
    padding: var(--size-3) var(--size-2);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
		flex-direction: column;
	} 

	p {
		font-size: var(--font-size-md);
	}

  section.chatform {
    position: absolute;
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
		box-shadow: var(--shadow-2);
    &:focus-within {
      border-color: var(--blue-3);
      outline: 2px solid var(--blue-4);
      outline-offset: 3px;
    }
  }

  :global(input, select, textarea) {
    padding: var(--size-2);
    font-size: var(--font-size-1);
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
    background: var(--gradient-2);
    border: none;
    color: white;
    transition: all 0.3s var(--ease-out-2);
    &:disabled {
      opacity: 0.6;
    }
  }
</style>
