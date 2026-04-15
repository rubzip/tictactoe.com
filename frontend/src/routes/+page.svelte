<script lang="ts">
    import { onMount } from "svelte";
    import { authStore } from "$lib/stores/auth";
    import { gameStore } from "$lib/stores/game";
    import { socketStore } from "$lib/stores/socket";
    import { goto } from "$app/navigation";
    import { Play, Loader2, Sword, Users, Zap, Cpu } from "lucide-svelte";

    let matchmaking = $derived($gameStore.matchmaking);
    let gameState = $derived($gameStore.state);
    let user = $derived($authStore.user);
    let joinRoomId = $state("");

    onMount(() => {
        socketStore.connect();
    });

    function handleJoinQueue() {
        if (!user) {
            goto("/login");
            return;
        }
        gameStore.joinQueue();
    }

    async function handleStartAiGame(
        difficulty: "EASY" | "MEDIUM" | "HARD" | "EXPERT",
    ) {
        try {
            const response = await fetch(
                `http://localhost:8000/api/v1/game/ai/start?difficulty=${difficulty}`,
                {
                    method: "POST",
                },
            );
            if (response.ok) {
                const data = await response.json();
                goto(`/game/${data.room_id}`);
            }
        } catch (error) {
            console.error("Failed to start AI game", error);
        }
    }

    async function handleCreateRoom() {
        try {
            const response = await fetch(
                "http://localhost:8000/api/v1/game/create",
                {
                    method: "POST",
                },
            );
            if (response.ok) {
                const data = await response.json();
                goto(`/game/${data.room_id}`);
            }
        } catch (error) {
            console.error("Failed to create room", error);
        }
    }

    $effect(() => {
        if ($gameStore.room_id && $gameStore.matchmaking.matchFound) {
            const targetRoom = $gameStore.room_id;
            gameStore.consumeMatch();
            goto(`/game/${targetRoom}`);
        }
    });
</script>

<div class="flex flex-col items-center py-12">
    <!-- Hero Section -->
    <div class="text-center">
        <h1 class="text-6xl font-black tracking-tight text-white sm:text-7xl">
            Play <span class="text-emerald-500">Fast.</span><br />
            Win <span class="text-amber-500">Big.</span>
        </h1>
        <p class="mt-6 text-xl text-zinc-400">
            The world's first competitive Tic-Tac-Toe platform.<br />
            Elo rankings, real-time matchmaking, and zero lag.
        </p>
    </div>

    <!-- Action Card -->
    <div
        class="mt-16 w-full max-w-2xl rounded-3xl border border-zinc-800 bg-zinc-900/50 p-12 shadow-2xl backdrop-blur-xl"
    >
        <div class="flex flex-col items-center gap-8">
            {#if matchmaking.searching}
                <div class="flex flex-col items-center gap-6">
                    <div class="relative">
                        <div
                            class="absolute inset-0 animate-ping rounded-full bg-emerald-500/20"
                        ></div>
                        <div
                            class="relative flex h-24 w-24 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-500"
                        >
                            <Loader2 size={48} class="animate-spin" />
                        </div>
                    </div>
                    <div class="text-center">
                        <h2 class="text-2xl font-bold text-white">
                            Searching for an opponent...
                        </h2>
                        <p class="text-zinc-500">
                            Finding someone at your skill level ({user?.elo_rating}
                            Elo)
                        </p>
                    </div>
                    <button
                        onclick={() => gameStore.leaveQueue()}
                        class="rounded-lg border border-zinc-700 bg-zinc-800 px-8 py-3 font-semibold text-white transition-all hover:bg-zinc-700"
                    >
                        Cancel
                    </button>
                </div>
            {:else}
                <div class="grid w-full grid-cols-1 gap-6 sm:grid-cols-2">
                    <button
                        onclick={handleJoinQueue}
                        class="group flex flex-col items-center gap-4 rounded-2xl bg-emerald-600 p-8 text-white transition-all hover:bg-emerald-500 hover:shadow-[0_0_30px_-10px_rgba(16,185,129,0.5)] active:scale-95"
                    >
                        <Play
                            size={48}
                            fill="currentColor"
                            class="transition-transform group-hover:scale-110"
                        />
                        <div class="text-center">
                            <span class="block text-xl font-bold"
                                >Quick Play</span
                            >
                            <span class="text-sm opacity-80"
                                >Ranked Matchmaking</span
                            >
                        </div>
                    </button>

                    <button
                        onclick={handleCreateRoom}
                        class="group flex flex-col items-center gap-4 rounded-2xl border border-zinc-700 bg-zinc-800 p-8 text-white transition-all hover:border-zinc-500 hover:bg-zinc-700 active:scale-95"
                    >
                        <Users
                            size={48}
                            class="transition-transform group-hover:scale-110"
                        />
                        <div class="text-center">
                            <span class="block text-xl font-bold"
                                >Play Friend</span
                            >
                            <span class="text-sm opacity-80"
                                >Invite via link</span
                            >
                        </div>
                    </button>
                </div>

                <div class="mt-8 w-full border-t border-zinc-800 pt-8">
                    <p
                        class="mb-4 text-center text-sm font-medium text-zinc-500"
                    >
                        Practice against the machine
                    </p>
                    <div class="grid grid-cols-3 gap-4">
                        <button
                            onclick={() => handleStartAiGame("EASY")}
                            class="flex flex-col items-center gap-2 rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4 text-emerald-500 transition-all hover:bg-emerald-500/10 active:scale-95"
                        >
                            <Cpu size={24} />
                            <span
                                class="text-xs font-bold uppercase tracking-wider text-emerald-400"
                                >Easy</span
                            >
                        </button>
                        <button
                            onclick={() => handleStartAiGame("MEDIUM")}
                            class="flex flex-col items-center gap-2 rounded-xl border border-amber-500/20 bg-amber-500/5 p-4 text-amber-500 transition-all hover:bg-amber-500/10 active:scale-95"
                        >
                            <Cpu size={24} />
                            <span
                                class="text-xs font-bold uppercase tracking-wider text-amber-400"
                                >Medium</span
                            >
                        </button>
                        <button
                            onclick={() => handleStartAiGame("EXPERT")}
                            class="flex flex-col items-center gap-2 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-red-500 transition-all hover:bg-red-500/10 active:scale-95"
                        >
                            <Cpu size={24} />
                            <span
                                class="text-xs font-bold uppercase tracking-wider text-red-400"
                                >Master</span
                            >
                        </button>
                    </div>
                </div>

                <div class="mt-8 w-full border-t border-zinc-800 pt-8">
                    <p
                        class="mb-4 text-center text-sm font-medium text-zinc-500"
                    >
                        Or join an existing room
                    </p>
                    <div class="flex gap-2">
                        <input
                            type="text"
                            bind:value={joinRoomId}
                            placeholder="Enter Room ID (e.g. match_1234)"
                            class="flex-1 rounded-lg border border-zinc-700 bg-zinc-800 px-4 py-3 text-white placeholder-zinc-500 focus:border-emerald-500 focus:outline-none"
                        />
                        <button
                            onclick={() =>
                                joinRoomId && goto(`/game/${joinRoomId}`)}
                            class="rounded-lg bg-zinc-700 px-6 py-3 font-semibold text-white transition-colors hover:bg-zinc-600"
                        >
                            Join
                        </button>
                    </div>
                </div>
            {/if}
        </div>

        <!-- Stats Grid -->
        <div
            class="mt-12 grid grid-cols-3 gap-8 border-t border-zinc-800 pt-12"
        >
            <div class="flex flex-col items-center text-center">
                <div class="mb-2 text-emerald-500"><Zap size={24} /></div>
                <span class="text-2xl font-bold text-white">50ms</span>
                <span class="text-xs uppercase tracking-widest text-zinc-500"
                    >Latency</span
                >
            </div>
            <div class="flex flex-col items-center text-center">
                <div class="mb-2 text-amber-500"><Sword size={24} /></div>
                <span class="text-2xl font-bold text-white">12,402</span>
                <span class="text-xs uppercase tracking-widest text-zinc-500"
                    >Games Today</span
                >
            </div>
            <div class="flex flex-col items-center text-center">
                <div class="mb-2 text-blue-500"><Users size={24} /></div>
                <span class="text-2xl font-bold text-white">842</span>
                <span class="text-xs uppercase tracking-widest text-zinc-500"
                    >Online Now</span
                >
            </div>
        </div>
    </div>
</div>
