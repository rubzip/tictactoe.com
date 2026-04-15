<script lang="ts">
    import { authStore } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { Mail, Lock, Loader2, AlertCircle } from "lucide-svelte";

    let username = $state("");
    let password = $state("");
    let error = $state("");
    let loading = $state(false);

    async function handleSubmit(e: SubmitEvent) {
        e.preventDefault();
        error = "";
        loading = true;

        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        try {
            await authStore.login(formData);
            goto("/");
        } catch (err: any) {
            error = err.message || "Invalid username or password";
        } finally {
            loading = false;
        }
    }
</script>

<div class="flex min-h-[60vh] items-center justify-center">
    <div
        class="w-full max-w-md space-y-8 rounded-2xl border border-zinc-800 bg-zinc-900/50 p-8 shadow-2xl backdrop-blur-xl"
    >
        <div class="text-center">
            <h1 class="text-3xl font-bold text-white">Welcome Back</h1>
            <p class="mt-2 text-zinc-400">Sign in to start playing</p>
        </div>

        {#if error}
            <div
                class="flex items-center gap-2 rounded-lg border border-red-900/50 bg-red-900/10 p-4 text-sm text-red-400"
            >
                <AlertCircle size={18} />
                <span>{error}</span>
            </div>
        {/if}

        <form onsubmit={handleSubmit} class="space-y-6">
            <div>
                <label
                    for="username"
                    class="block text-sm font-medium text-zinc-400"
                    >Username</label
                >
                <div class="group relative mt-1">
                    <div
                        class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-zinc-500 transition-colors group-focus-within:text-emerald-500"
                    >
                        <Mail size={18} />
                    </div>
                    <input
                        id="username"
                        type="text"
                        bind:value={username}
                        required
                        class="block w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2.5 pl-10 pr-3 text-white placeholder-zinc-500 focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500 transition-all"
                        placeholder="user_1"
                    />
                </div>
            </div>

            <div>
                <label
                    for="password"
                    class="block text-sm font-medium text-zinc-400"
                    >Password</label
                >
                <div class="group relative mt-1">
                    <div
                        class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-zinc-500 transition-colors group-focus-within:text-emerald-500"
                    >
                        <Lock size={18} />
                    </div>
                    <input
                        id="password"
                        type="password"
                        bind:value={password}
                        required
                        class="block w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2.5 pl-10 pr-3 text-white placeholder-zinc-500 focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500 transition-all"
                        placeholder="••••••••"
                    />
                </div>
            </div>

            <button
                type="submit"
                disabled={loading}
                class="flex w-full items-center justify-center gap-2 rounded-lg bg-emerald-600 py-3 font-semibold text-white transition-all hover:bg-emerald-500 active:scale-[0.98] disabled:opacity-50 disabled:active:scale-100"
            >
                {#if loading}
                    <Loader2 size={20} class="animate-spin" />
                    <span>Signing in...</span>
                {:else}
                    <span>Sign In</span>
                {/if}
            </button>
        </form>

        <p class="text-center text-sm text-zinc-500">
            Don't have an account?
            <a
                href="/register"
                class="font-medium text-emerald-500 hover:text-emerald-400"
                >Sign up</a
            >
        </p>
    </div>
</div>
