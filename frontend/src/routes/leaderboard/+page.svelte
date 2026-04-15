<script lang="ts">
    import { onMount } from "svelte";
    import { Trophy, Medal, Star, User } from "lucide-svelte";
    import { getAvatarUrl } from "$lib/stores/auth";

    interface LeaderboardItem {
        username: string;
        elo_rating: number;
        wins: number;
        played_games: number;
    }

    let players = $state<LeaderboardItem[]>([]);
    let loading = $state(true);
    let error = $state<string | null>(null);

    onMount(async () => {
        try {
            const response = await fetch(
                "http://localhost:8000/api/v1/leaderboards/",
            );
            if (response.ok) {
                const data = await response.json();
                players = data.items.map((item: any) => ({
                    username: item.username,
                    elo_rating: item.elo || 0, // Backend might return 'elo'
                    wins: 0, // Placeholder if backend doesn't return wins here
                    played_games: 0,
                }));
            } else {
                error = "Failed to load leaderboard";
            }
        } catch (err) {
            error = "Connection error";
        } finally {
            loading = false;
        }
    });

    const getMedalColor = (index: number) => {
        if (index === 0) return "text-amber-400"; // Gold
        if (index === 1) return "text-zinc-300"; // Silver
        if (index === 2) return "text-amber-600"; // Bronze
        return "text-zinc-600";
    };
</script>

<div class="mx-auto max-w-4xl py-12">
    <div class="mb-12 flex items-center justify-between">
        <div>
            <h1 class="text-4xl font-black text-white">Global Leaderboard</h1>
            <p class="mt-2 text-zinc-400">
                The world's best Tic-Tac-Toe players.
            </p>
        </div>
        <div
            class="flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-500/10 text-amber-500"
        >
            <Trophy size={40} />
        </div>
    </div>

    {#if loading}
        <div class="flex h-64 items-center justify-center">
            <div
                class="h-12 w-12 animate-spin rounded-full border-4 border-emerald-500 border-t-transparent"
            ></div>
        </div>
    {:else if error}
        <div
            class="rounded-xl border border-red-500/20 bg-red-500/10 p-8 text-center text-red-400"
        >
            {error}
        </div>
    {:else}
        <div
            class="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900/50 backdrop-blur-sm"
        >
            <table class="w-full text-left">
                <thead>
                    <tr
                        class="border-b border-zinc-800 bg-zinc-900/80 text-xs font-bold uppercase tracking-wider text-zinc-500"
                    >
                        <th class="px-6 py-4">Rank</th>
                        <th class="px-6 py-4">Player</th>
                        <th class="px-6 py-4 text-right">Rating</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-zinc-800">
                    {#each players as player, i}
                        <tr
                            class="group transition-colors hover:bg-zinc-800/50"
                        >
                            <td class="px-6 py-5">
                                <div class="flex items-center gap-2">
                                    {#if i < 3}
                                        <Medal
                                            size={20}
                                            class={getMedalColor(i)}
                                        />
                                    {:else}
                                        <span
                                            class="w-5 text-center text-sm font-bold text-zinc-600"
                                            >{i + 1}</span
                                        >
                                    {/if}
                                </div>
                            </td>
                            <td class="px-6 py-5">
                                <a
                                    href={`/profile/${player.username}`}
                                    class="group/item flex items-center gap-4"
                                >
                                    <div
                                        class="h-10 w-10 overflow-hidden rounded-full border border-zinc-800 bg-zinc-950 transition-transform group-hover/item:scale-110"
                                    >
                                        <img
                                            src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${player.username}`}
                                            alt={player.username}
                                            class="h-full w-full object-cover"
                                        />
                                    </div>
                                    <span
                                        class="font-bold text-white transition-colors group-hover/item:text-emerald-400"
                                        >{player.username}</span
                                    >
                                </a>
                            </td>
                            <td class="px-6 py-5 text-right">
                                <div
                                    class="flex items-center justify-end gap-2 text-xl font-black text-white"
                                >
                                    <Star
                                        size={16}
                                        class="fill-amber-400 text-amber-400"
                                    />
                                    <span>{player.elo_rating}</span>
                                </div>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>
