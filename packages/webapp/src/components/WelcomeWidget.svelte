<script>
  import { fly } from 'svelte/transition';
</script>

<article out:fly={{ y: -12, duration: 225 }}>
  <h2>What is this?</h2>
  <p>
    This is an AI chat bot trained on my blog, 
    <a href="https://mykal.codes/">mykal.codes</a>.  
    This allows you to effectively "chat" with the content of my blog. 
    <i>Which I think is pretty sweet.</i>
  </p>
  <p>
    The end-goal would of this project be a chatbot that could speak
    semi-intelligently about my interests. You can already ask it for my
    thoughts on docker, or how to make an aeropress latte; It should respond
    with a summary and links to my blog for more info.
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
