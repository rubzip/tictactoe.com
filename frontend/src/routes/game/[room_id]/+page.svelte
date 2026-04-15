<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { page } from "$app/state";
    import { gameStore } from "$lib/stores/game";
    import { socketStore } from "$lib/stores/socket";
    import { getAvatarUrl } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import Board from "$lib/components/Board.svelte";
    import Chat from "$lib/components/Chat.svelte";
    import { Trophy, ChevronLeft, AlertCircle } from "lucide-svelte";

    const room_id = $derived(page.params.room_id as string);
    const game = $derived($gameStore.state);
    const role = $derived($gameStore.role);
    const error = $derived($gameStore.error);

    const opponentRole = $derived(role === "X" ? "O" : "X");

    const getPlayerName = (r: "X" | "O") => {
        const username = game?.player_usernames[r];
        if (username) return username;

        const aiDiff = game?.ai_difficulties[r];
        if (aiDiff) return `AI (${aiDiff.toLowerCase()})`;

        return "Waiting...";
    };

    const getPlayerAvatar = (r: "X" | "O") => {
        const username = game?.player_usernames[r];
        if (username) return getAvatarUrl({ username });
        const aiDiff = game?.ai_difficulties[r];
        if (aiDiff)
            return `https://api.dicebear.com/7.x/bottts-neutral/svg?seed=${aiDiff}`;
        return `https://api.dicebear.com/7.x/avataaars/svg?seed=placeholder`;
    };

    onMount(() => {
        socketStore.connect();
        if (room_id) {
            gameStore.joinRoom(room_id);
        }
    });

    // Auto-redirect on error after 5 seconds
    $effect(() => {
        if (error) {
            const timer = setTimeout(() => {
                gameStore.reset();
                goto("/");
            }, 5000);
            return () => clearTimeout(timer);
        }
    });

    onDestroy(() => {
        gameStore.reset();
    });
</script>

<div class="grid grid-cols-1 gap-8 lg:grid-cols-12">
    <!-- Left Side: Navigation and Status -->
    <div class="lg:col-span-3">
        <a
            href="/"
            class="flex items-center gap-2 text-zinc-500 hover:text-white transition-colors mb-8"
        >
            <ChevronLeft size={20} />
            <span>Back to Menu</span>
        </a>

        <div class="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
            <h2
                class="text-sm font-bold uppercase tracking-widest text-zinc-500"
            >
                Room Info
            </h2>
            <div class="mt-4 space-y-4">
                <div>
                    <span class="text-xs text-zinc-600">Room ID</span>
                    <p class="font-mono text-sm text-zinc-300">{room_id}</p>
                </div>
                <div>
                    <span class="text-xs text-zinc-600">Your Role</span>
                    <p class="font-bold text-emerald-500">
                        {role || "Spectating"}
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- Center: Game Board -->
    <div class="flex flex-col items-center gap-8 lg:col-span-6">
        <!-- Opponent Info -->
        <div
            class="flex w-full items-center justify-between rounded-2xl bg-zinc-900/50 p-4 border border-zinc-800"
        >
            <div class="flex items-center gap-3">
                <div
                    class="h-10 w-10 overflow-hidden rounded-full border border-zinc-800 bg-zinc-950"
                >
                    <img
                        src={getPlayerAvatar(opponentRole)}
                        alt="Opponent"
                        class="h-full w-full object-cover"
                    />
                </div>
                <div>
                    <p
                        class="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-0.5"
                    >
                        Opponent
                    </p>
                    <p class="font-bold text-white">
                        {getPlayerName(opponentRole)}
                    </p>
                </div>
            </div>
            {#if game?.turn === opponentRole && game.status === "KEEP_PLAYING"}
                <div
                    class="rounded-full bg-amber-500/20 px-3 py-1 text-xs font-bold text-amber-500 animate-pulse"
                >
                    Thinking...
                </div>
            {/if}
        </div>

        <Board {room_id} />

        <!-- My Info -->
        <div
            class="flex w-full items-center justify-between rounded-2xl bg-zinc-900/50 p-4 border border-zinc-800"
        >
            <div class="flex items-center gap-3">
                <div
                    class="h-10 w-10 overflow-hidden rounded-full border border-zinc-800 bg-zinc-950"
                >
                    <img
                        src={getPlayerAvatar((role as "X" | "O") || "X")}
                        alt="Me"
                        class="h-full w-full object-cover"
                    />
                </div>
                <div>
                    <p
                        class="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-0.5"
                    >
                        You
                    </p>
                    <p class="font-bold text-white">
                        {getPlayerName((role as "X" | "O") || "X")}
                    </p>
                </div>
            </div>
            {#if game?.turn === role && game.status === "KEEP_PLAYING"}
                <div
                    class="rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-bold text-emerald-500 animate-pulse"
                >
                    Your Turn!
                </div>
            {/if}
        </div>
    </div>

    <!-- Right Side: Chat -->
    <div class="h-[600px] lg:col-span-3">
        <Chat />
    </div>
</div>

{#if error}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-zinc-950/80 backdrop-blur-md"
    >
        <div
            class="max-w-md rounded-3xl border border-red-500/20 bg-zinc-900 p-12 text-center shadow-2xl"
        >
            <div
                class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-red-500/10 text-red-500"
            >
                <AlertCircle size={48} />
            </div>
            <h2 class="mb-2 text-2xl font-black text-white">Room Error</h2>
            <p class="mb-8 text-zinc-400">{error}</p>
            <button
                onclick={() => {
                    gameStore.reset();
                    goto("/");
                }}
                class="w-full rounded-xl bg-red-600 py-4 font-bold text-white transition-all hover:bg-red-500 active:scale-95"
            >
                Return Home
            </button>
            <p class="mt-4 text-[10px] uppercase tracking-widest text-zinc-600">
                Redirecting in 5 seconds...
            </p>
        </div>
    </div>
{/if}
