<script lang="ts">
	import { authStore, getAvatarUrl } from "$lib/stores/auth";
	import {
		LogIn,
		LogOut,
		Trophy,
		User as UserIcon,
		LayoutDashboard,
		BarChart3,
	} from "lucide-svelte";

	let user = $derived($authStore.user);
</script>

<nav class="border-b border-zinc-800 bg-zinc-950 px-6 py-4">
	<div class="mx-auto flex max-w-6xl items-center justify-between">
		<div class="flex items-center gap-12">
			<a
				href="/"
				class="flex items-center gap-2 text-2xl font-bold text-emerald-500"
			>
				<div class="grid grid-cols-2 gap-0.5">
					<div class="h-3 w-3 rounded-sm bg-emerald-500"></div>
					<div class="h-3 w-3 rounded-sm bg-zinc-700"></div>
					<div class="h-3 w-3 rounded-sm bg-zinc-700"></div>
					<div class="h-3 w-3 rounded-sm bg-emerald-500"></div>
				</div>
				<span>tictactoe<span class="text-zinc-400">.com</span></span>
			</a>

			<div class="hidden items-center gap-6 md:flex">
				<a
					href="/leaderboard"
					class="flex items-center gap-2 text-sm font-medium text-zinc-400 transition-colors hover:text-white"
				>
					<Trophy size={16} />
					Leaderboard
				</a>
				<a
					href={user ? `/profile/${user.username}` : "/login"}
					class="flex items-center gap-2 text-sm font-medium text-zinc-400 transition-colors hover:text-white"
				>
					<BarChart3 size={16} />
					Profile
				</a>
			</div>
		</div>

		<div class="flex items-center gap-6">
			{#if user}
				<div class="flex items-center gap-4">
					<div class="flex flex-col items-end">
						<span class="text-sm font-medium text-zinc-200"
							>{user.username}</span
						>
						<div
							class="flex items-center gap-1 text-xs text-zinc-500"
						>
							<Trophy size={12} class="text-amber-500" />
							<span>{user.elo_rating}</span>
						</div>
					</div>
					<a
						href={`/profile/${user.username}`}
						class="h-10 w-10 overflow-hidden rounded-full border border-zinc-800 bg-zinc-900 transition-transform hover:scale-105 active:scale-95"
					>
						<img
							src={getAvatarUrl(user)}
							alt={user.username}
							class="h-full w-full object-cover"
						/>
					</a>
					<button
						onclick={() => authStore.logout()}
						class="flex items-center gap-2 text-zinc-400 hover:text-white"
					>
						<LogOut size={18} />
					</button>
				</div>
			{:else}
				<a
					href="/login"
					class="flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 font-medium text-white transition-colors hover:bg-emerald-500"
				>
					<LogIn size={18} />
					<span>Login</span>
				</a>
			{/if}
		</div>
	</div>
</nav>
