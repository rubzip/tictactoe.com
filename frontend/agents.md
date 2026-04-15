# Project Overview
tictactoe.com is a competitive multiplayer platform. It is a "chess.com clone" applied to Tic-Tac-Toe, focusing on real-time gameplay, clean UI, and social interaction.

## Tech Stack
- Frontend: Svelte (with SvelteKit)

- Styling: Tailwind CSS

- Real-time: WebSockets (for game state and chat)

- Icons: Lucide-Svelte

- State Management: Svelte Stores

## Core Features
- Real-time Board: A 3x3 grid that updates instantly via WebSockets.

- Live Chat: Sidebar or overlay chat for players within a match.

- Auth Flow: Simple Login and Sign-up (JWT or Session based).

- Matchmaking: Logic to handle joining rooms or finding opponents.

## UI/UX Guidelines (Chess.com Aesthetic)
- Palette: Dark mode by default. Use Slate/Zinc for backgrounds, Emerald/Green for primary actions, and Wood/Earth tones for the board if applicable.

- Layout: Centered game board with a sidebar for "Move List," "Chat," and "Player Stats."

- Feedback: Clear visual indicators for whose turn it is and highlighting the winning line.

## Development Rules & Patterns
- Svelte Idioms: Use $: reactive declarations for derived state (e.g., checking if the board is full).

- WebSocket Logic: Centralize socket events in a dedicated Svelte Store (socketStore.ts) to avoid redundant listeners.

- Component Architecture:

    - Board.svelte: Handles grid rendering and click events.

    - Chat.svelte: Manages message history and input.

    - AuthForm.svelte: Reusable component for Login/Register.

- Tailwind Only: Avoid writing custom CSS in <style> tags unless doing complex animations. Use class:name={condition} for dynamic styling.

- Type Safety: Use TypeScript interfaces for GameSession, User, and SocketMessage.

## Project Structure (Preferences)
- /src/lib/components: For reusable UI components.

- /src/lib/stores: For global state (socket, user, game).

- /src/routes: SvelteKit file-based routing.