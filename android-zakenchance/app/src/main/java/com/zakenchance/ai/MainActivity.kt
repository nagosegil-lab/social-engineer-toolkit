package com.zakenchance.ai

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.weight
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import kotlin.math.min
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                ZakenChanceApp()
            }
        }
    }
}

@Composable
private fun ZakenChanceApp() {
    val context = LocalContext.current
    val clipboard = LocalClipboardManager.current
    val scope = rememberCoroutineScope()
    val settingsRepository = remember(context) { SettingsRepository(context) }

    val persistedState by settingsRepository.uiState.collectAsState(initial = PersistedUiState())

    val lottoModes = remember {
        listOf(
            "Balanced Distribution",
            "Anti-Crowd Mode",
            "Hot + Cold Mix",
            "Random",
        )
    }
    val chanceModes = remember {
        listOf(
            "Balanced Distribution",
            "History Weighted",
            "Hot + Cold Mix",
            "Random",
        )
    }

    var hydratedFromStorage by rememberSaveable { mutableStateOf(false) }
    var selectedTab by rememberSaveable { mutableIntStateOf(0) }

    var pastLottoInput by rememberSaveable { mutableStateOf(persistedState.pastLottoInput) }
    var pastChanceInput by rememberSaveable { mutableStateOf(persistedState.pastChanceInput) }
    var budgetInput by rememberSaveable { mutableStateOf("30") }
    var ticketPriceInput by rememberSaveable { mutableStateOf("3") }
    var lottoAmount by rememberSaveable { mutableIntStateOf(5) }
    var chanceAmount by rememberSaveable { mutableIntStateOf(5) }
    var lottoMode by rememberSaveable { mutableStateOf(lottoModes.first()) }
    var chanceMode by rememberSaveable { mutableStateOf(chanceModes.first()) }

    val generatedLotto = remember { mutableStateListOf<GeneratedLottoTicket>() }
    val generatedChance = remember { mutableStateListOf<Map<String, String>>() }

    LaunchedEffect(persistedState, hydratedFromStorage) {
        if (!hydratedFromStorage) {
            pastLottoInput = persistedState.pastLottoInput
            pastChanceInput = persistedState.pastChanceInput
            budgetInput = persistedState.budget.toString()
            ticketPriceInput = persistedState.ticketPrice.toString()
            lottoAmount = persistedState.lottoAmount
            chanceAmount = persistedState.chanceAmount
            lottoMode = if (persistedState.lottoMode in lottoModes) {
                persistedState.lottoMode
            } else {
                lottoModes.first()
            }
            chanceMode = if (persistedState.chanceMode in chanceModes) {
                persistedState.chanceMode
            } else {
                chanceModes.first()
            }
            hydratedFromStorage = true
        }
    }

    val lottoParse = remember(pastLottoInput) { parseLottoHistory(pastLottoInput) }
    val chanceParse = remember(pastChanceInput) { parseChanceHistory(pastChanceInput) }

    val budget = budgetInput.toIntOrNull() ?: 0
    val ticketPrice = ticketPriceInput.toIntOrNull() ?: 0
    val maxTicketsByBudget = if (ticketPrice > 0) budget / ticketPrice else 0
    val allowedLottoMax = min(50, maxTicketsByBudget.coerceAtLeast(1))
    val safeLottoAmount = lottoAmount.coerceIn(1, allowedLottoMax)
    val safeChanceAmount = chanceAmount.coerceIn(1, 20)

    LaunchedEffect(
        hydratedFromStorage,
        pastLottoInput,
        pastChanceInput,
        budget,
        ticketPrice,
        safeLottoAmount,
        safeChanceAmount,
        lottoMode,
        chanceMode,
    ) {
        if (hydratedFromStorage) {
            settingsRepository.save(
                PersistedUiState(
                    pastLottoInput = pastLottoInput,
                    pastChanceInput = pastChanceInput,
                    budget = budget,
                    ticketPrice = ticketPrice,
                    lottoAmount = safeLottoAmount,
                    chanceAmount = safeChanceAmount,
                    lottoMode = lottoMode,
                    chanceMode = chanceMode,
                ),
            )
        }
    }

    LaunchedEffect(allowedLottoMax, lottoAmount) {
        if (safeLottoAmount != lottoAmount) {
            lottoAmount = safeLottoAmount
        }
    }
    LaunchedEffect(chanceAmount) {
        if (safeChanceAmount != chanceAmount) {
            chanceAmount = safeChanceAmount
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.primaryContainer,
            ),
        ) {
            Column(
                modifier = Modifier.padding(14.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Text("🎲 ZakenChance AI Analyzer", style = MaterialTheme.typography.headlineSmall)
                Text("לשימוש בידורי וסטטיסטי בלבד. אין הבטחת זכייה.")
                Button(onClick = {
                    pastLottoInput = ""
                    pastChanceInput = ""
                    budgetInput = "30"
                    ticketPriceInput = "3"
                    lottoAmount = 5
                    chanceAmount = 5
                    lottoMode = lottoModes.first()
                    chanceMode = chanceModes.first()
                    generatedLotto.clear()
                    generatedChance.clear()
                    scope.launch {
                        settingsRepository.clear()
                    }
                }) {
                    Text("נקה קלט ותוצאות")
                }
            }
        }

        TabRow(
            selectedTabIndex = selectedTab,
            modifier = Modifier
                .fillMaxWidth()
                .background(MaterialTheme.colorScheme.surfaceVariant),
        ) {
            Tab(selected = selectedTab == 0, onClick = { selectedTab = 0 }, text = { Text("לוטו") })
            Tab(selected = selectedTab == 1, onClick = { selectedTab = 1 }, text = { Text("צ׳אנס") })
        }

        if (selectedTab == 0) {
            SectionCard(title = "📥 תוצאות עבר - לוטו") {
                OutlinedTextField(
                    value = pastLottoInput,
                    onValueChange = { pastLottoInput = it },
                    label = { Text("כל שורה: 6 מספרים + חזק") },
                    placeholder = { Text("1,7,19,22,27,34 | 5") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                )
                if (lottoParse.invalidRows.isNotEmpty()) {
                    ValidationCard(
                        title = "שורות לוטו שנפסלו (${lottoParse.invalidRows.size})",
                        rows = lottoParse.invalidRows,
                    )
                }

                if (lottoParse.lottoNumbers.isNotEmpty()) {
                    HorizontalDivider()
                    val counts = lottoParse.lottoNumbers.groupingBy { it }.eachCount()
                    val hot = counts.entries.sortedByDescending { it.value }.take(10)
                    val cold = ALL_LOTTO_NUMBERS.sortedBy { counts[it] ?: 0 }.take(10)
                    val strongStats = lottoParse.strongNumbers.groupingBy { it }.eachCount()
                        .entries.sortedByDescending { it.value }
                    Text("🔥 חמים: ${hot.joinToString { "${it.key}(${it.value})" }}")
                    Text("❄️ קרים: ${cold.joinToString(", ")}")
                    Text("💪 חזק נפוץ: ${strongStats.joinToString { "${it.key}(${it.value})" }}")
                }
            }

            SectionCard(title = "🤖 מחולל לוטו AI") {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = budgetInput,
                        onValueChange = { budgetInput = it.filter { ch -> ch.isDigit() } },
                        label = { Text("תקציב") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                    )
                    OutlinedTextField(
                        value = ticketPriceInput,
                        onValueChange = { ticketPriceInput = it.filter { ch -> ch.isDigit() } },
                        label = { Text("מחיר לטופס") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                    )
                }

                if (maxTicketsByBudget <= 0) {
                    Text("התקציב לא מספיק אפילו לטופס אחד.", color = MaterialTheme.colorScheme.error)
                } else {
                    Text("מקסימום לפי תקציב: ${min(50, maxTicketsByBudget)} טפסים")
                    CounterRow(
                        label = "כמות טפסים",
                        value = lottoAmount,
                        min = 1,
                        max = allowedLottoMax,
                        onDecrease = { lottoAmount = (lottoAmount - 1).coerceAtLeast(1) },
                        onIncrease = { lottoAmount = (lottoAmount + 1).coerceAtMost(allowedLottoMax) },
                    )
                }

                ModeSelector(
                    title = "מצב לוטו",
                    options = lottoModes,
                    selected = lottoMode,
                    onSelected = { lottoMode = it },
                )

                Button(
                    onClick = {
                        generatedLotto.clear()
                        generatedLotto.addAll(
                            generateMultiTickets(
                                amount = safeLottoAmount,
                                mode = lottoMode,
                                lottoNumbers = lottoParse.lottoNumbers,
                                strongNumbers = lottoParse.strongNumbers,
                            ),
                        )
                    },
                    enabled = maxTicketsByBudget > 0,
                ) {
                    Text("צור טפסי לוטו AI")
                }
            }

            if (generatedLotto.isNotEmpty()) {
                SectionCard(title = "🎯 טפסי לוטו שנוצרו") {
                    Text("נוצרו ${generatedLotto.size} טפסים")
                    generatedLotto.forEach { ticket ->
                        Card(modifier = Modifier.fillMaxWidth()) {
                            Column(
                                modifier = Modifier.padding(10.dp),
                                verticalArrangement = Arrangement.spacedBy(4.dp),
                            ) {
                                Text("טופס ${ticket.index}: ${ticket.numbers} | חזק: ${ticket.strong}")
                                Text("ציון AI: ${ticket.details.score}/100")
                                Text(
                                    "זוגיים: ${ticket.details.evens}, נמוכים: ${ticket.details.lows}, " +
                                        "סכום: ${ticket.details.total}, רצפים: ${ticket.details.adjacentPairs}",
                                )
                                Text(
                                    "הורדות ציון: ${
                                        ticket.details.penalties.joinToString(", ").ifBlank { "ללא הורדות" }
                                    }",
                                )
                            }
                        }
                    }
                    Button(
                        onClick = {
                            clipboard.setText(AnnotatedString(lottoCsv(generatedLotto)))
                            Toast.makeText(context, "CSV לוטו הועתק ללוח", Toast.LENGTH_SHORT).show()
                        },
                    ) {
                        Text("העתק CSV לוטו")
                    }
                }
            }
        } else {
            SectionCard(title = "📥 תוצאות עבר - צ׳אנס") {
                OutlinedTextField(
                    value = pastChanceInput,
                    onValueChange = { pastChanceInput = it },
                    label = { Text("כל שורה: תלתן,יהלום,לב,עלה") },
                    placeholder = { Text("10,K,8,J") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                )
                if (chanceParse.invalidRows.isNotEmpty()) {
                    ValidationCard(
                        title = "שורות צ׳אנס שנפסלו (${chanceParse.invalidRows.size})",
                        rows = chanceParse.invalidRows,
                    )
                }

                if (chanceParse.draws.isNotEmpty()) {
                    HorizontalDivider()
                    val counters = chanceSuitCounters(chanceParse.draws)
                    CHANCE_SUITS.forEach { suit ->
                        val suitCounts = counters[suit].orEmpty()
                        val hot = suitCounts.entries.sortedByDescending { it.value }.take(3)
                        val cold = CHANCE_CARDS.sortedBy { suitCounts[it] ?: 0 }.take(3)
                        Text(
                            "$suit | חמים: ${hot.joinToString { "${it.key}(${it.value})" }} | " +
                                "קרים: ${cold.joinToString(", ")}",
                        )
                    }
                }
            }

            SectionCard(title = "🃏 מחולל צ׳אנס AI") {
                CounterRow(
                    label = "כמות טפסי צ׳אנס",
                    value = chanceAmount,
                    min = 1,
                    max = 20,
                    onDecrease = { chanceAmount = (chanceAmount - 1).coerceAtLeast(1) },
                    onIncrease = { chanceAmount = (chanceAmount + 1).coerceAtMost(20) },
                )

                ModeSelector(
                    title = "מצב צ׳אנס",
                    options = chanceModes,
                    selected = chanceMode,
                    onSelected = { chanceMode = it },
                )

                Button(
                    onClick = {
                        generatedChance.clear()
                        generatedChance.addAll(
                            generateMultiChanceTickets(
                                amount = safeChanceAmount,
                                mode = chanceMode,
                                draws = chanceParse.draws,
                            ),
                        )
                    },
                ) {
                    Text("צור טפסי צ׳אנס AI")
                }
            }

            if (generatedChance.isNotEmpty()) {
                SectionCard(title = "🎯 טפסי צ׳אנס שנוצרו") {
                    Text("נוצרו ${generatedChance.size} טפסי צ׳אנס")
                    generatedChance.forEachIndexed { index, ticket ->
                        Text(
                            "טופס ${index + 1}: ${
                                CHANCE_SUITS.joinToString(" | ") { suit -> "$suit: ${ticket[suit]}" }
                            }",
                        )
                    }
                    Button(
                        onClick = {
                            clipboard.setText(AnnotatedString(chanceCsv(generatedChance)))
                            Toast.makeText(context, "CSV צ׳אנס הועתק ללוח", Toast.LENGTH_SHORT).show()
                        },
                    ) {
                        Text("העתק CSV צ׳אנס")
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(4.dp))
        Text("ZakenChance AI — ניתוח סטטיסטי לכיף בלבד.")
    }
}

@Composable
private fun SectionCard(title: String, content: @Composable Column.() -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
        ),
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            content()
        }
    }
}

@Composable
private fun ValidationCard(title: String, rows: List<String>) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.errorContainer,
        ),
    ) {
        Column(modifier = Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(title, style = MaterialTheme.typography.titleSmall)
            rows.take(8).forEach { row ->
                Text("• $row")
            }
            if (rows.size > 8) {
                Text("... ועוד ${rows.size - 8} שורות")
            }
        }
    }
}

@Composable
private fun CounterRow(
    label: String,
    value: Int,
    min: Int,
    max: Int,
    onDecrease: () -> Unit,
    onIncrease: () -> Unit,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Text(label, modifier = Modifier.padding(top = 10.dp))
        TextButton(onClick = onDecrease, enabled = value > min) { Text("-") }
        Text(value.toString(), modifier = Modifier.padding(top = 10.dp))
        TextButton(onClick = onIncrease, enabled = value < max) { Text("+") }
    }
}

@Composable
private fun ModeSelector(
    title: String,
    options: List<String>,
    selected: String,
    onSelected: (String) -> Unit,
) {
    Text(title, style = MaterialTheme.typography.titleSmall)
    options.forEach { option ->
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Start,
        ) {
            RadioButton(
                selected = selected == option,
                onClick = { onSelected(option) },
            )
            Text(option, modifier = Modifier.padding(top = 12.dp))
        }
    }
}
