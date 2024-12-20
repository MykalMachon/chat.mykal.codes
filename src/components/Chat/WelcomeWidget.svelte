<script>
  import { fly } from 'svelte/transition';
</script>

<article out:fly={{ y: -12, duration: 225 }}>
  <h2>What is this?</h2>
  <p>
    This was an RAG-powered chatbot using posts from my blog. 
    It initially used Langchain as a backend. I later replaced Langchain with <a href="https://langbase.com/">Langbase</a>.
  </p>
  <p>
    I shut this down on <time datetime="2024-12-20">December 20th, 2024</time> as I wasn't keeping up with it.
    Ideally I'll come back and update this to a modern RAG setup sometime soon. 
  </p>

  <h2>Other links</h2>
  <ul>
    <li>
      <a href="https://github.com/MykalMachon/chat.mykal.codes/">Source Code</a
      >: check out the repo on GitHub.
    </li>
    <li>
      <a href="https://mykal.codes/">Source Content</a>: my blog.
    </li>
  </ul>
</article>

<style>
  article {
    max-width: 800px;
    width: 100%;
  }

  a {
    color: var(--acc-3);
    text-decoration: none;
    &:hover {
      text-decoration: underline;
    }
  }
</style>
