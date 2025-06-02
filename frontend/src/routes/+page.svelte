<script>
  import { onMount } from 'svelte';

  let source = '';
  let destination = '';
  let distance = null;
  let errorMessage = '';
  let history = [];

  async function fetchDistance() {
    errorMessage = '';
    distance = null;
    try {
      const res = await fetch('http://localhost:8000/distance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, destination })
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to fetch distance');
      }
      const data = await res.json();
      distance = data.distance_km;
      await fetchHistory();
    } catch (err) {
      errorMessage = err.message;
    }
  }

  async function fetchHistory() {
    try {
      const res = await fetch('http://localhost:8000/history');
      if (res.ok) {
        history = await res.json();
      }
    } catch (e) {
      console.error('Failed to fetch history', e);
    }
  }

  onMount(() => {
    fetchHistory();
  });
</script>

<h1>Distance Query</h1>
<div>
  <input placeholder="Source Address" bind:value={source} />
  <input placeholder="Destination Address" bind:value={destination} />
  <button on:click={fetchDistance}>Calculate</button>
</div>
{#if errorMessage}
  <p style="color:red;">{errorMessage}</p>
{/if}
{#if distance !== null}
  <p>Distance: {distance.toFixed(2)} km</p>
{/if}

<h2>Past Queries</h2>
<table>
  <thead>
    <tr>
      <th>Source</th>
      <th>Destination</th>
      <th>Distance (km)</th>
      <th>Time</th>
    </tr>
  </thead>
  <tbody>
    {#each history as record}
      <tr>
        <td>{record.source}</td>
        <td>{record.destination}</td>
        <td>{record.distance_km.toFixed(2)}</td>
        <td>{new Date(record.timestamp).toLocaleString()}</td>
      </tr>
    {/each}
  </tbody>
</table>
