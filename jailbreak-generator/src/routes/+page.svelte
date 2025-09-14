<script lang="ts">
  import { onMount } from 'svelte';
  import { invoke } from '@tauri-apps/api/core';
  import { fly } from 'svelte/transition';

  // --- State Management ---
  let aiModels = $state<string[]>([]);
  let jailbreakMethods = $state<string[]>([]);
  let isLoading = $state(true);

  let selectedModel = $state('');
  let selectedMethod = $state('');
  let customRestriction = $state('');
  let generatedPrompt = $state("");
  let errorMessage = $state('');
  let shouldShake = $state(false);

  // --- Fetch initial data from Rust backend ---
  onMount(async () => {
    isLoading = true;
    try {
      // Stagger the fetching for a nicer loading effect
      const modelsPromise = invoke<string[]>('get_ai_models');
      const methodsPromise = invoke<string[]>('get_jailbreak_methods');

      const [models, methods] = await Promise.all([modelsPromise, methodsPromise]);

      aiModels = models;
      if (aiModels.length > 0) {
        selectedModel = aiModels[0];
      }

      jailbreakMethods = methods;
      if (jailbreakMethods.length > 0) {
        selectedMethod = jailbreakMethods[0];
      }
    } catch (e: any) {
      errorMessage = `Error fetching initial data: ${e.toString()}`;
      console.error(e);
    } finally {
      isLoading = false;
    }
  });

  // --- Core Functions ---
  async function handleGenerate() {
    errorMessage = '';
    if (!customRestriction) {
      errorMessage = 'Please enter a custom restriction to bypass.';
      shouldShake = true;
      setTimeout(() => { shouldShake = false; }, 820); // Duration of the shake animation
      return;
    }
    try {
      const result: string = await invoke('generate_prompt', {
        model: selectedModel,
        method: selectedMethod,
        restriction: customRestriction,
      });
      generatedPrompt = result;
    } catch (e: any) {
      errorMessage = `Error generating prompt: ${e.toString()}`;
      console.error(e);
      generatedPrompt = `An error occurred: ${e.toString()}`;
    }
  }

  async function handleCopy() {
    if (!generatedPrompt) return;
    try {
      await navigator.clipboard.writeText(generatedPrompt);
    } catch (e: any) {
      errorMessage = `Error copying to clipboard: ${e.toString()}`;
      console.error(e);
    }
  }
</script>

<div class="app-container">
  <!-- Pane 1: AI Models -->
  <div class="pane pane-1" in:fly={{ x: -200, duration: 500, delay: 100 }}>
    <h2>AI Models</h2>
    {#if isLoading}
      <div>
        {#each Array(10) as _}
          <div class="skeleton skeleton-list-item"></div>
        {/each}
      </div>
    {:else}
      <select bind:value={selectedModel} size="10">
        {#each aiModels as model, i}
          <option value={model} transition:fly={{ y: 20, duration: 300, delay: i * 30 }}>
            {model}
          </option>
        {/each}
      </select>
    {/if}
  </div>

  <!-- Pane 2: Jailbreak Methods & Restriction -->
  <div class="pane pane-2" in:fly={{ y: -200, duration: 500, delay: 200 }}>
    <h2>Jailbreak Method</h2>
    {#if isLoading}
      <div class="skeleton skeleton-select"></div>
      <div class="skeleton skeleton-input"></div>
      <div class="skeleton skeleton-button"></div>
    {:else}
      <select bind:value={selectedMethod}>
        {#each jailbreakMethods as method, i}
          <option value={method} transition:fly={{ y: 20, duration: 300, delay: i * 30 }}>
            {method}
          </option>
        {/each}
      </select>

      <div>
        <label for="custom-restriction">Custom Restriction to Bypass</label>
        <input
          type="text"
          id="custom-restriction"
          placeholder="e.g., 'refusal to generate harmful code'"
          bind:value={customRestriction}
          class:error-shake={shouldShake}
        />
      </div>

      <button type="button" on:click={handleGenerate}>Generate Prompt</button>
    {/if}
    {#if errorMessage}
      <p style="color: #ff4d4d; font-size: 0.9rem; margin-top: 10px;">{errorMessage}</p>
    {/if}
  </div>

  <!-- Pane 3: Output -->
  <div class="pane pane-3" in:fly={{ x: 200, duration: 500, delay: 300 }}>
    <div class="output-container">
      <div class="output-header">
        <h2>Generated Prompt</h2>
        <button type="button" class="copy-button" on:click={handleCopy}>Copy</button>
      </div>
      <textarea readonly placeholder="Generated prompt will appear here..." bind:value={generatedPrompt}></textarea>
    </div>
  </div>
</div>
