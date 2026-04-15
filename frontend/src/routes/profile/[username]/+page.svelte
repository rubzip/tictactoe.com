<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/state";
    import { getAvatarUrl } from "$lib/stores/auth";
    import {
        BarChart3,
        TrendingUp,
        History,
        Trophy,
        Sword,
        Target,
        Loader2,
    } from "lucide-svelte";
    import { goto } from "$app/navigation";

    // @ts-ignore - SvelteKit params can be tricky with types in dev
    let username = $derived(page.params.username as string);
    let targetUser = $state<any>(null);
    let history = $state<any[]>([]);
    let loading = $state(true);
    let error = $state<string | null>(null);

    async function fetchProfile() {
        loading = true;
        error = null;
        try {
            // 1. Fetch User Data
            const userRes = await fetch(
                `http://localhost:8000/api/v1/users/${username}`,
            );
            if (userRes.ok) {
                targetUser = await userRes.json();
            } else {
                error = "User not found";
                return;
            }

            // 2. Fetch Match History
            const historyRes = await fetch(
                `http://localhost:8000/api/v1/users/${username}/history`,
            );
            if (historyRes.ok) {
                const data = await historyRes.json();
                history = data.matches || [];
            }
        } catch (err) {
            error = "Failed to load profile";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        fetchProfile();
    });

    // Re-fetch if username changes
    $effect(() => {
        if (username) fetchProfile();
    });

    const getStatusColor = (status: string, role: string) => {
        if (status === "DRAW") return "text-zinc-400 bg-zinc-400/10";
        if (
            (status === "X_WINS" && role === "X") ||
            (status === "O_WINS" && role === "O")
        )
            return "text-emerald-400 bg-emerald-400/10";
        return "text-red-400 bg-red-400/10";
    };
</script>

<div class="mx-auto max-w-5xl py-12 px-6">
    {#if loading && !targetUser}
        <div class="flex h-64 items-center justify-center">
            <Loader2 size={48} class="animate-spin text-emerald-500" />
        </div>
    {:else if error}
        <div
            class="rounded-2xl border border-red-500/20 bg-red-500/10 p-12 text-center text-red-400"
        >
            <h2 class="text-2xl font-bold">{error}</h2>
            <button
                onclick={() => goto("/")}
                class="mt-4 text-sm font-medium hover:underline"
                >Return Home</button
            >
        </div>
    {:else if targetUser}
        <div class="mb-12 flex flex-col gap-8 md:flex-row md:items-center">
            <div
                class="h-32 w-32 overflow-hidden rounded-3xl border-4 border-zinc-800 bg-zinc-900 shadow-2xl"
            >
                <img
                    src={getAvatarUrl(targetUser)}
                    alt={targetUser.username}
                    class="h-full w-full object-cover"
                />
            </div>
            <div>
                <h1 class="text-5xl font-black text-white">
                    {targetUser.username}
                </h1>
                <div class="mt-2 flex items-center gap-4">
                    <span class="flex items-center gap-1 text-zinc-400">
                        <Trophy size={16} class="text-amber-500" />
                        {targetUser.elo_rating} Elo
                    </span>
                    <span class="text-zinc-700">|</span>
                    <span class="text-emerald-500 font-medium">Top Player</span>
                </div>
            </div>
        </div>

        <!-- Quick Stats Grid -->
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div
                class="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur-sm"
            >
                <div class="mb-3 text-emerald-500"><Trophy size={20} /></div>
                <div class="text-3xl font-black text-white">
                    {targetUser.elo_rating}
                </div>
                <div
                    class="text-xs font-bold uppercase tracking-widest text-zinc-500"
                >
                    Current Rating
                </div>
            </div>
            <div
                class="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur-sm"
            >
                <div class="mb-3 text-amber-500"><Sword size={20} /></div>
                <div class="text-3xl font-black text-white">
                    {targetUser.played_games}
                </div>
                <div
                    class="text-xs font-bold uppercase tracking-widest text-zinc-500"
                >
                    Games Played
                </div>
            </div>
            <div
                class="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur-sm"
            >
                <div class="mb-3 text-blue-500"><Target size={20} /></div>
                <div class="text-3xl font-black text-white">
                    {targetUser.won_games}
                </div>
                <div
                    class="text-xs font-bold uppercase tracking-widest text-zinc-500"
                >
                    Total Wins
                </div>
            </div>
            <div
                class="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6 backdrop-blur-sm"
            >
                <div class="mb-3 text-zinc-400"><TrendingUp size={20} /></div>
                <div class="text-3xl font-black text-white">
                    {targetUser.played_games > 0
                        ? Math.round(
                              (targetUser.won_games / targetUser.played_games) *
                                  100,
                          )
                        : 0}%
                </div>
                <div
                    class="text-xs font-bold uppercase tracking-widest text-zinc-500"
                >
                    Win Rate
                </div>
            </div>
        </div>

        <div class="mt-16">
            <h2
                class="mb-8 flex items-center gap-3 text-2xl font-bold text-white"
            >
                <History size={24} class="text-emerald-500" />
                Battle History
            </h2>

            {#if history.length === 0}
                <div
                    class="rounded-3xl border border-dashed border-zinc-800 p-20 text-center text-zinc-500"
                >
                    This warrior hasn't fought any battles yet.
                </div>
            {:else}
                <div class="grid gap-3">
                    {#each history as match}
                        {@const role =
                            match.player_x_username === targetUser.username
                                ? "X"
                                : "O"}
                        {@const isWin =
                            (match.status === "X_WINS" && role === "X") ||
                            (match.status === "O_WINS" && role === "O")}
                        {@const isDraw = match.status === "DRAW"}
                        <div
                            class="group flex items-center justify-between rounded-2xl border border-zinc-800 bg-zinc-900/30 p-5 transition-all hover:border-zinc-700 hover:bg-zinc-800/40"
                        >
                            <div class="flex items-center gap-6">
                                <div
                                    class={`flex h-12 w-24 items-center justify-center rounded-xl text-sm font-black uppercase tracking-widest ${getStatusColor(match.status, role)} shadow-sm`}
                                >
                                    {isDraw
                                        ? "Draw"
                                        : isWin
                                          ? "Victory"
                                          : "Defeat"}
                                </div>
                                <div class="flex flex-col">
                                    <span
                                        class="font-bold text-white transition-colors group-hover:text-emerald-400"
                                    >
                                        vs {role === "X"
                                            ? match.player_o_username || "AI"
                                            : match.player_x_username}
                                    </span>
                                    <span
                                        class="text-xs font-medium text-zinc-500"
                                        >{new Date(
                                            match.created_at || Date.now(),
                                        ).toLocaleDateString("en-GB", {
                                            day: "numeric",
                                            month: "short",
                                            year: "numeric",
                                        })}</span
                                    >
                                </div>
                            </div>
                            <div class="flex items-center gap-6">
                                <div class="hidden text-right sm:block">
                                    <span
                                        class="block text-[10px] font-bold uppercase tracking-widest text-zinc-600"
                                        >Session ID</span
                                    >
                                    <span
                                        class="font-mono text-xs text-zinc-500"
                                        >{match.room_id}</span
                                    >
                                </div>
                                <button
                                    onclick={() =>
                                        goto(`/game/${match.room_id}`)}
                                    class="rounded-xl bg-zinc-800 px-6 py-3 text-sm font-bold text-zinc-200 transition-colors hover:bg-emerald-600 hover:text-white"
                                >
                                    Replay
                                </button>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    {/if}
</div>
