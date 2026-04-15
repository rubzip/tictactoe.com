<script lang="ts">
    import { gameStore } from "$lib/stores/game";
    import { authStore } from "$lib/stores/auth";
    import { socketStore } from "$lib/stores/socket";
    import { X, Circle } from "lucide-svelte";

    let { room_id } = $props<{ room_id: string }>();

    let game = $derived($gameStore.state);
    let role = $derived($gameStore.role);
    let isMyTurn = $derived(
        game && game.status === "KEEP_PLAYING" && game.turn === role,
    );

    function handleClick(row: number, col: number) {
        if (isMyTurn && game && game.board[row][col] === "") {
            gameStore.makeMove(row, col);
        }
    }

    function isWinCell(row: number, col: number) {
        return game?.win_line?.some(([r, c]) => r === row && c === col);
    }
</script>

<div
    class="relative aspect-square w-full max-w-md overflow-hidden rounded-xl border-4 border-zinc-800 bg-zinc-900 shadow-2xl"
>
    <!-- Grid Lines -->
    <div class="absolute inset-0 grid grid-cols-3 grid-rows-3">
        {#each Array(3) as _, row}
            {#each Array(3) as _, col}
                <button
                    onclick={() => handleClick(row, col)}
                    disabled={!isMyTurn ||
                        !game ||
                        !game.board ||
                        game.board[row][col] !== ""}
                    class="group relative flex items-center justify-center border border-zinc-800/50 transition-all hover:bg-zinc-800/30 disabled:cursor-not-allowed {isWinCell(
                        row,
                        col,
                    )
                        ? 'bg-emerald-500/10'
                        : ''}"
                >
                    {#if game?.board[row][col] === "X"}
                        <div
                            class="text-emerald-500"
                            class:animate-bounce-short={isWinCell(row, col)}
                        >
                            <X size={64} strokeWidth={3} />
                        </div>
                    {:else if game?.board[row][col] === "O"}
                        <div
                            class="text-amber-500"
                            class:animate-bounce-short={isWinCell(row, col)}
                        >
                            <Circle size={60} strokeWidth={3} />
                        </div>
                    {:else if isMyTurn}
                        <div
                            class="opacity-0 transition-opacity group-hover:opacity-20"
                        >
                            {#if role === "X"}
                                <X size={48} />
                            {:else}
                                <Circle size={44} />
                            {/if}
                        </div>
                    {/if}
                </button>
            {/each}
        {/each}
    </div>

    <!-- Overlay for Game Over -->
    {#if game && game.status !== "KEEP_PLAYING"}
        <div
            class="absolute inset-0 z-10 flex flex-col items-center justify-center bg-zinc-950/60 backdrop-blur-sm transition-all"
        >
            <h2 class="text-4xl font-extrabold text-white">
                {#if game.status === "X_WINS"}
                    <span class="text-emerald-500">X Wins!</span>
                {:else if game.status === "O_WINS"}
                    <span class="text-amber-500">O Wins!</span>
                {:else}
                    <span class="text-zinc-400">Draw!</span>
                {/if}
            </h2>
            <button
                onclick={() => gameStore.reset()}
                class="mt-6 rounded-full bg-white px-8 py-3 font-bold text-black transition-transform hover:scale-105"
            >
                Find New Match
            </button>
        </div>
    {/if}
</div>

<style>
    @keyframes bounce-short {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-5px);
        }
    }
    .animate-bounce-short {
        animation: bounce-short 0.5s ease-in-out infinite;
    }
</style>
