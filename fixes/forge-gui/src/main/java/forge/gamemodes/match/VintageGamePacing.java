package forge.gamemodes.match;

import com.google.common.eventbus.Subscribe;
import forge.ai.PlayerControllerAi;
import forge.game.Game;
import forge.game.event.GameEventLandPlayed;
import forge.game.event.GameEventSpellAbilityCast;
import forge.game.event.GameEventTurnPhase;
import forge.game.player.Player;
import forge.gui.FThreads;

import java.util.HashSet;
import java.util.Set;

/** Presentation pacing for a human playing Vintage Solo, never AI simulations. */
public final class VintageGamePacing {
    private static final int CARD_DELAY_MS = 1000;
    private static final int PHASE_DELAY_MS = 500;
    private final Set<Integer> botIds = new HashSet<>();

    public VintageGamePacing(final Game game) {
        for (Player player : game.getPlayers()) {
            if (player.getController() instanceof PlayerControllerAi) {
                botIds.add(player.getId());
            }
        }
    }

    @Subscribe
    public void onLand(final GameEventLandPlayed event) {
        if (botIds.contains(event.player().getId())) {
            pause(CARD_DELAY_MS);
        }
    }

    @Subscribe
    public void onSpell(final GameEventSpellAbilityCast event) {
        // Do not delay each mana activation, trigger, copy, or priority pass.
        if (event.sa().isSpell() && botIds.contains(event.si().getActivatingPlayer().getId())) {
            pause(CARD_DELAY_MS);
        }
    }

    @Subscribe
    public void onPhase(final GameEventTurnPhase event) {
        if (botIds.contains(event.playerTurn().getId())) {
            pause(PHASE_DELAY_MS);
        }
    }

    private static void pause(final int milliseconds) {
        // Forge posts these events synchronously from its game thread. Its UI
        // event subscriber has already queued repaint work; rendering stays live.
        if (FThreads.isGuiThread()) {
            return;
        }
        try {
            Thread.sleep(milliseconds);
        } catch (InterruptedException interrupted) {
            Thread.currentThread().interrupt();
        }
    }
}
