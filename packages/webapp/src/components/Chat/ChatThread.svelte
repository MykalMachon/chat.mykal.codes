<script>
  import WelcomeWidget from './WelcomeWidget.svelte';
  import { thread, threadLoading } from '../../utils/stores';
  import ChatMessage from './ChatMessage.svelte';
</script>

<main>
  {#if $thread.length == 0}
    <WelcomeWidget />
  {/if}

  <div class="chat-message__container">
    {#each $thread as { type, text }, i}
      <ChatMessage type={type} text={text} />
    {/each}
    {#if $threadLoading}
      <ChatMessage type={'loading'} text='' />
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

  @media screen and (max-width: 800px) {
    div.chat-message__container {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>
