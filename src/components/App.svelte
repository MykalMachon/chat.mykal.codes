<script>
  import Nav from './Layout/Nav.svelte';
  import ChatThread from './Chat/ChatThread.svelte';
  import ChatForm from './Chat/ChatForm.svelte';
</script>

<div class="site-container">
  <Nav />
  <ChatThread />
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

    --acc-1: var(--blue-12);
    --acc-2: var(--blue-10);
    --acc-3: var(--blue-8);
    --acc-4: var(--blue-6);
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

      --acc-1: var(--blue-1);
      --acc-2: var(--blue-3);
      --acc-3: var(--blue-6);
      --acc-4: var(--blue-8);
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

  :global(p, li) {
    font-size: var(--font-size-base);
    line-height: 1.5;
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

  .site-container {
    height: 100vh;
    display: grid;
    grid-template-rows: auto 1fr auto;
  }
</style>
