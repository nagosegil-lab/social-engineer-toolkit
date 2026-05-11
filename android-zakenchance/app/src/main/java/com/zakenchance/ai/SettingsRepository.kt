package com.zakenchance.ai

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore by preferencesDataStore(name = "zakenchance_settings")

data class PersistedUiState(
    val pastLottoInput: String = "",
    val pastChanceInput: String = "",
    val budget: Int = 30,
    val ticketPrice: Int = 3,
    val lottoAmount: Int = 5,
    val chanceAmount: Int = 5,
    val lottoMode: String = "Balanced Distribution",
    val chanceMode: String = "Balanced Distribution",
)

class SettingsRepository(private val context: Context) {
    private val pastLottoInputKey = stringPreferencesKey("past_lotto_input")
    private val pastChanceInputKey = stringPreferencesKey("past_chance_input")
    private val budgetKey = intPreferencesKey("budget")
    private val ticketPriceKey = intPreferencesKey("ticket_price")
    private val lottoAmountKey = intPreferencesKey("lotto_amount")
    private val chanceAmountKey = intPreferencesKey("chance_amount")
    private val lottoModeKey = stringPreferencesKey("lotto_mode")
    private val chanceModeKey = stringPreferencesKey("chance_mode")

    val uiState: Flow<PersistedUiState> = context.dataStore.data.map { preferences ->
        PersistedUiState(
            pastLottoInput = preferences[pastLottoInputKey] ?: "",
            pastChanceInput = preferences[pastChanceInputKey] ?: "",
            budget = preferences[budgetKey] ?: 30,
            ticketPrice = preferences[ticketPriceKey] ?: 3,
            lottoAmount = preferences[lottoAmountKey] ?: 5,
            chanceAmount = preferences[chanceAmountKey] ?: 5,
            lottoMode = preferences[lottoModeKey] ?: "Balanced Distribution",
            chanceMode = preferences[chanceModeKey] ?: "Balanced Distribution",
        )
    }

    suspend fun save(state: PersistedUiState) {
        context.dataStore.edit { preferences ->
            preferences[pastLottoInputKey] = state.pastLottoInput
            preferences[pastChanceInputKey] = state.pastChanceInput
            preferences[budgetKey] = state.budget
            preferences[ticketPriceKey] = state.ticketPrice
            preferences[lottoAmountKey] = state.lottoAmount
            preferences[chanceAmountKey] = state.chanceAmount
            preferences[lottoModeKey] = state.lottoMode
            preferences[chanceModeKey] = state.chanceMode
        }
    }

    suspend fun clear() {
        context.dataStore.edit { preferences ->
            preferences.clear()
        }
    }
}
