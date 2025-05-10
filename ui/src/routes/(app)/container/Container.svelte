<script>
	import { Dot, ScrollText, ChevronRight, Info, RotateCcw } from '@lucide/svelte';

	const {isFirst,isLast} = $props()
	$inspect(isLast)
</script>

<main>
	<div class:first={isFirst} class:last={isLast} class:middle={!isFirst && !isLast}>
		<div class="container">
		<Dot class="status" size="100" color="green" />
		<span class="name">Container</span>
		<div class="actions">
			<ScrollText class="action" size="32" color="var(--white)" />
			<ChevronRight class="action" size="32" color="var(--white)" />
			<Info class="action" size="32" color="var(--white)" />
			<RotateCcw class="action" size="32" color="var(--white)" />
		</div>
		<span class="node">Node</span>
	</div>
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';


  .first {
    background-color: pallet.$primary;
    border-top-right-radius: 10px;

		border-bottom: white solid 1px;
  }

	.middle {
		background-color: pallet.$primary;
		border-bottom: none;
    border-bottom: white solid 1px;
	}

  .last{
    background-color: pallet.$primary;
    border-bottom: none;
    border-bottom-right-radius: 10px;
  }
main {
		width: 100%;

  .container {
    background-color: pallet.$primary;
    width: 90%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;

    .actions {
      display: flex;
      flex-direction: row;
      gap: 1rem;
    }

    span {
      font-size: 1.2rem;
      color: pallet.$white;
    }

  }
}
</style>
