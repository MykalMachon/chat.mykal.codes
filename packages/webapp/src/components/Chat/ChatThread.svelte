<script>
  import { fly } from 'svelte/transition';
  import WelcomeWidget from './WelcomeWidget.svelte';
  import { thread, threadLoading } from '../../utils/stores';
</script>

<main>
  {#if $thread.length == 0}
    <WelcomeWidget />
  {/if}

  <div class="chat-message__container">
    {#each $thread as { type, text, sources }, i}
      <div
        in:fly={{
          y: 12,
          duration: 450,
          delay: i === 0 || i === 1 ? 226 : 0,
        }}
        class={`chat-message ${type}`}
      >
        <p>
          {text}
        </p>
        {#if sources}
          <aside class="source">
            <p>source: {sources}</p>
          </aside>
        {/if}
      </div>
    {/each}
    {#if $threadLoading}
      <div
        in:fly={{
          y: 12,
          duration: 450,
          delay: $thread.length === 1 ? 226 : 0,
        }}
        class="chat-message answer"
      >
        <p>Let me think about that...🤔</p>
      </div>
    {/if}
  </div>
</main>

<style>
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
    }

    & aside.source {
      margin-top: var(--size-2);
      padding-top: var(--size-2);
      border-top: 1px solid var(--acc-4);
      font-style: italic;
      color: var(--ink-4);
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
</style>
