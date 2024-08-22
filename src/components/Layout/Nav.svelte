<script>
  import IoLogoGithub from 'svelte-icons/io/IoLogoGithub.svelte';
  import IoIosJournal from 'svelte-icons/io/IoIosJournal.svelte';

  import { fly } from 'svelte/transition';
  import { thread } from '../../utils/stores';
</script>

<nav>
  <div class="nav__container">
    <div class="nav__container__item icon">
      {#if $thread.length > 0}
        <a
          in:fly={{
            x: -12,
            duration: 450,
          }}
          href="https://mykal.codes/posts/"
          title="view source content"
        >
          <IoIosJournal />
        </a>
      {/if}
    </div>
    <div class="nav__container__item"><h1>chat.mykal.codes</h1></div>
    <div class="nav__container__item icon">
      {#if $thread.length > 0}
        <a
          in:fly={{
            x: 12,
            duration: 450,
          }}
          href="https://github.com/mykalmachon/chat.mykal.codes/"
          title="view project source code"
        >
          <IoLogoGithub />
        </a>
      {/if}
    </div>
  </div>
</nav>

<style>
  nav {
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid var(--paper-4);
    padding: var(--size-1) var(--size-2);
    background: var(--paper-2);

    & h1 {
      font-size: var(--font-size-base);
      font-family: var(--font-mono);
      font-weight: bold;
      text-transform: uppercase;
      letter-spacing: var(--size-1);
    }

    & .nav__container {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
      max-width: 800px;
      width: 100%;
    }

    & .icon {
      width: 40px;
      height: 40px;
      padding: var(--size-2);
      display: inline-flex;
      align-items: center;
      justify-content: center;

      & a {
        color: var(--ink-1);
        opacity: 0.5;
        transition: opacity 0.3s ease-in-out;
        &:hover {
          opacity: 1;
        }
      }
    }
  }
</style>
