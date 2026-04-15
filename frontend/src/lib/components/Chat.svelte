<script lang="ts">
    import { gameStore } from "$lib/stores/game";
    import { Send } from "lucide-svelte";
    import { tick } from "svelte";

    let message = $state("");
    let chatContainer: HTMLElement | undefined = $state();

    const chat = $derived($gameStore.chat);

    async function handleSubmit(e: SubmitEvent) {
        e.preventDefault();
        if (!message.trim()) return;

        gameStore.sendMessage(message);
        message = "";

        await tick();
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }

    $effect(() => {
        if (chat.length && chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    });
</script>

<div
    class="flex h-full flex-col rounded-xl border border-zinc-800 bg-zinc-900/40"
>
    <div class="border-b border-zinc-800 p-3">
        <h3 class="font-semibold text-zinc-400">Room Chat</h3>
    </div>

    <div
        bind:this={chatContainer}
        class="flex-1 space-y-3 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-zinc-700"
    >
        {#each chat as msg}
            <div class="flex flex-col">
                <div class="flex items-baseline gap-2">
                    <span class="text-xs font-bold text-emerald-500"
                        >{msg.username}</span
                    >
                    <span class="text-[10px] text-zinc-600">now</span>
                </div>
                <p class="text-sm text-zinc-200">{msg.message}</p>
            </div>
        {/each}
        {#if chat.length === 0}
            <div
                class="flex h-full flex-col items-center justify-center text-center opacity-20"
            >
                <Send size={48} />
                <p class="mt-2 text-sm">Say hello to your opponent!</p>
            </div>
        {/if}
    </div>

    <form onsubmit={handleSubmit} class="border-t border-zinc-800 p-3">
        <div class="relative">
            <input
                type="text"
                bind:value={message}
                placeholder="Type a message..."
                class="w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2 pl-3 pr-10 text-sm text-white focus:border-emerald-500 focus:outline-none"
            />
            <button
                type="submit"
                class="absolute right-1 top-1 rounded-md p-1.5 text-emerald-500 transition-colors hover:bg-emerald-500/10"
            >
                <Send size={18} />
            </button>
        </div>
    </form>
</div>
