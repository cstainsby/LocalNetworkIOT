

<script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    interface DogTrackerDataInstance {
        timestamp: Date,
        postitionX: number,
        postitionY: number,
        positionZ: number
    }

    let mostRecentData: DogTrackerDataInstance = {
        timestamp: new Date(),
        postitionX: 200.2,
        postitionY: 152.75,
        positionZ: 2
    }


    // every hundred seconds update the most recent data
    const interval = setInterval(() => {
        mostRecentData
    }, 10000)


    onMount(() => {
        // Clear the interval when the component is destroyed
        onDestroy(() => {
            clearInterval(interval);
        });
  });
</script>

<h1>Dog Tracker Project</h1>
<p>Ever wonder what the dog doin, well heres the answer.</p>

<p>For this project </p>

<div>
    <h2>Live Updates</h2>
    {#if mostRecentData}
        <p>As of {JSON.stringify(mostRecentData)} </p>
    {:else}
        <p>Loading</p>
    {/if}
</div>

<div>
    <h2>Data</h2>

    <div>
        <h3>Data Shape</h3>
        <ul>
            <li><b>Timestamp</b> - Datetime denoting when the data was recorded</li>
            <li><b>PositionX</b> - Float denoting x position of dog</li>
            <li><b>PositionY</b> - Float denoting y position of dog</li>
            <li><b>PositionZ</b> - Float denoting z position of dog</li>
        </ul>
    </div>
    <button>Download</button>
</div>
