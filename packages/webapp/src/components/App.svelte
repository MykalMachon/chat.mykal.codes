<script>
	const API_BASE = "https://chat-api-production-cb57.up.railway.app/api/chat/"
	
	let question = ""
	let answer = null;
	let loading = false;

	const submitQuestionForm = async (e) => {
		e.preventDefault();
		loading = true;
		
		// get data from form as object
		const form = new FormData(e.target);
		const formData = Object.fromEntries(form.entries())

		// construct URL params 
		const params = new URLSearchParams(formData)
		const apiUrl = new URL(`${API_BASE}?${params.toString()}`)

		// call the API 
		const res = await fetch(apiUrl);
		const data = await res.json();

		answer = data;
		loading = false;
	}
</script>

<h1>Mykal.<code>ai</code> Chat</h1>

<section>
	{#if !answer}
		<p>no results</p>
	{:else}
		<p>
			{answer.answer}
		</p>
		<p>
			sources: 
			{answer.sources}
		</p>
	{/if}
</section>

<form on:submit={submitQuestionForm} method="GET" target="https://chat-api-production-cb57.up.railway.app/api/chat/">
	<input type="text" id="q" name="q" bind:value={question} />
	<button type="submit" disabled='{question.length <= 0 || loading}'>
		{#if loading} 
			loading...
		{:else}
			{#if question.length <= 0}
				Type a question!
			{:else}
				Ask a question!
			{/if}
		{/if}
	</button>
</form>
