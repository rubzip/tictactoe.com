import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export interface User {
    username: string;
    email: string;
    avatar_url?: string;
    elo_rating: number;
    played_games: number;
    won_games: number;
    lost_games: number;
}

interface AuthState {
    user: User | null;
    token: string | null;
    loading: boolean;
}

export const getAvatarUrl = (user: { username?: string; avatar_url?: string } | null) => {
    if (!user) return `https://api.dicebear.com/7.x/avataaars/svg?seed=guest`;
    if (user.avatar_url) return user.avatar_url;
    return `https://api.dicebear.com/7.x/avataaars/svg?seed=${user.username}`;
};

const API_BASE = 'http://localhost:8000/api/v1';

const createAuthStore = () => {
    const initialToken = browser ? localStorage.getItem('token') : null;
    const { subscribe, set, update } = writable<AuthState>({
        user: null,
        token: initialToken,
        loading: !!initialToken
    });

    return {
        subscribe,
        login: async (formData: FormData) => {
            update((s) => ({ ...s, loading: true }));
            try {
                const params = new URLSearchParams();
                for (const [key, value] of formData.entries()) {
                    params.append(key, value as string);
                }

                const response = await fetch(`${API_BASE}/auth/token`, {
                    method: 'POST',
                    body: params
                });

                if (!response.ok) throw new Error('Login failed');

                const data = await response.json();
                const token = data.access_token;

                if (browser) localStorage.setItem('token', token);

                update((s) => ({ ...s, token, loading: true }));
                await authStore.fetchUser(token);
            } catch (error) {
                update((s) => ({ ...s, loading: false }));
                throw error;
            }
        },
        register: async (userData: any) => {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Registration failed');
            }
        },
        fetchUser: async (token: string) => {
            try {
                const response = await fetch(`${API_BASE}/users/me`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (response.ok) {
                    const user = await response.json();
                    update((s) => ({ ...s, user, loading: false }));
                } else {
                    authStore.logout();
                }
            } catch (error) {
                authStore.logout();
            }
        },
        logout: () => {
            if (browser) localStorage.removeItem('token');
            set({ user: null, token: null, loading: false });
        },
        init: async () => {
            if (initialToken) {
                await authStore.fetchUser(initialToken);
            } else {
                update((s) => ({ ...s, loading: false }));
            }
        }
    };
};

export const authStore = createAuthStore();
