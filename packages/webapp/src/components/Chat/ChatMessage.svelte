<script>
  export let type;
  export let text;

  import { fly } from 'svelte/transition';
  import * as showdown from 'showdown';
  
  import { newMessageStream } from '../../utils/stores';

  const converter = new showdown.Converter();
</script>

<article 
  in:fly={{y: 12, duration: 450, delay: 225}}
  class={`chat-message ${type}`}>
  {#if type === 'error' || type === 'question'}
    <p>{text}</p>
  {/if}

  {#if type === 'loading'}
    {#if $newMessageStream}
      <p>{@html converter.makeHtml($newMessageStream)}</p>
    {:else}
      <p>💭</p>
    {/if}
  {/if}

  {#if type === 'answer'}
    <p>{@html converter.makeHtml(text)}</p>
  {/if}
</article>

<style>
  article.chat-message {
    position: relative;
    grid-column: 2/6;
    padding: var(--size-3);
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

    &:is(.answer, .error, .loading) {
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
    article.chat-message {
      width: 100%;
    }
  }
</style>
