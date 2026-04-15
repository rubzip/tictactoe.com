<script lang="ts">
	import { onMount } from "svelte";
	import { authStore } from "$lib/stores/auth";
	import Navbar from "$lib/components/Navbar.svelte";
	import "./layout.css";

	let { children } = $props();

	onMount(() => {
		authStore.init();
	});
</script>

<div class="min-h-screen bg-zinc-950 text-zinc-100">
	<Navbar />
	<main class="mx-auto max-w-6xl p-6">
		{@render children()}
	</main>
</div>
