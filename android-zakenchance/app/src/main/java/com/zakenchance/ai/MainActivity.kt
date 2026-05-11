package com.zakenchance.ai

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.Divider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import kotlin.math.min

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

    var pastLottoInput by rememberSaveable { mutableStateOf("") }
    var pastChanceInput by rememberSaveable { mutableStateOf("") }
    var budgetInput by rememberSaveable { mutableStateOf("30") }
    var ticketPriceInput by rememberSaveable { mutableStateOf("3") }
    var lottoAmount by rememberSaveable { mutableIntStateOf(5) }
    var chanceAmount by rememberSaveable { mutableIntStateOf(5) }
    var lottoMode by rememberSaveable { mutableStateOf("Balanced Distribution") }
    var chanceMode by rememberSaveable { mutableStateOf("Balanced Distribution") }

    val generatedLotto = remember { mutableStateListOf<GeneratedLottoTicket>() }
    val generatedChance = remember { mutableStateListOf<Map<String, String>>() }

    val lottoParse = remember(pastLottoInput) { parseLottoHistory(pastLottoInput) }
    val chanceParse = remember(pastChanceInput) { parseChanceHistory(pastChanceInput) }

    val budget = budgetInput.toIntOrNull() ?: 0
    val ticketPrice = ticketPriceInput.toIntOrNull() ?: 0
    val maxTicketsByBudget = if (ticketPrice > 0) budget / ticketPrice else 0
    val allowedLottoMax = min(50, maxTicketsByBudget.coerceAtLeast(1))
    val safeLottoAmount = lottoAmount.coerceIn(1, allowedLottoMax)
    val safeChanceAmount = chanceAmount.coerceIn(1, 20)

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
        Text("🎲 ZakenChance AI Analyzer", style = MaterialTheme.typography.headlineSmall)
        Text(
            "לשימוש בידורי וסטטיסטי בלבד. אין הבטחת זכייה.",
            style = MaterialTheme.typography.bodyMedium,
        )

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = {
                pastLottoInput = ""
                pastChanceInput = ""
                generatedLotto.clear()
                generatedChance.clear()
            }) {
                Text("נקה קלט ותוצאות")
            }
        }

        Divider()
        Text("📥 תוצאות עבר", style = MaterialTheme.typography.titleMedium)

        OutlinedTextField(
            value = pastLottoInput,
            onValueChange = { pastLottoInput = it },
            label = { Text("לוטו: כל שורה 6 מספרים + חזק") },
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

        OutlinedTextField(
            value = pastChanceInput,
            onValueChange = { pastChanceInput = it },
            label = { Text("צ׳אנס: כל שורה 4 קלפים (תלתן,יהלום,לב,עלה)") },
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

        if (lottoParse.lottoNumbers.isNotEmpty()) {
            Divider()
            Text("📊 ניתוח תוצאות עבר - לוטו", style = MaterialTheme.typography.titleMedium)
            val counts = lottoParse.lottoNumbers.groupingBy { it }.eachCount()
            val hot = counts.entries.sortedByDescending { it.value }.take(10)
            val cold = ALL_LOTTO_NUMBERS.sortedBy { counts[it] ?: 0 }.take(10)
            val strongStats = lottoParse.strongNumbers.groupingBy { it }.eachCount()
                .entries.sortedByDescending { it.value }

            Text("🔥 חמים: ${hot.joinToString { "${it.key}(${it.value})" }}")
            Text("❄️ קרים: ${cold.joinToString(", ")}")
            Text("💪 חזק נפוץ: ${strongStats.joinToString { "${it.key}(${it.value})" }}")
        }

        if (chanceParse.draws.isNotEmpty()) {
            Divider()
            Text("📊 ניתוח תוצאות עבר - צ׳אנס", style = MaterialTheme.typography.titleMedium)
            val counters = chanceSuitCounters(chanceParse.draws)
            CHANCE_SUITS.forEach { suit ->
                val suitCounts = counters[suit].orEmpty()
                val hot = suitCounts.entries.sortedByDescending { it.value }.take(3)
                val cold = CHANCE_CARDS.sortedBy { suitCounts[it] ?: 0 }.take(3)
                Text("$suit | חמים: ${hot.joinToString { "${it.key}(${it.value})" }} | קרים: ${cold.joinToString(", ")}")
            }
        }

        Divider()
        Text("🤖 מחולל לוטו AI", style = MaterialTheme.typography.titleMedium)

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
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("כמות טפסים:")
                TextButton(onClick = { if (lottoAmount > 1) lottoAmount -= 1 }) { Text("-") }
                Text(lottoAmount.toString(), modifier = Modifier.padding(top = 12.dp))
                TextButton(onClick = { if (lottoAmount < allowedLottoMax) lottoAmount += 1 }) { Text("+") }
            }
        }

        ModeSelector(
            title = "מצב לוטו",
            options = listOf(
                "Balanced Distribution",
                "Anti-Crowd Mode",
                "Hot + Cold Mix",
                "Random",
            ),
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

        if (generatedLotto.isNotEmpty()) {
            Text("נוצרו ${generatedLotto.size} טפסים", style = MaterialTheme.typography.titleSmall)
            generatedLotto.forEach { ticket ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
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

        Divider()
        Text("🃏 מחולל צ׳אנס AI", style = MaterialTheme.typography.titleMedium)

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Text("כמות טפסי צ׳אנס:")
            TextButton(onClick = { if (chanceAmount > 1) chanceAmount -= 1 }) { Text("-") }
            Text(chanceAmount.toString(), modifier = Modifier.padding(top = 12.dp))
            TextButton(onClick = { if (chanceAmount < 20) chanceAmount += 1 }) { Text("+") }
        }

        ModeSelector(
            title = "מצב צ׳אנס",
            options = listOf(
                "Balanced Distribution",
                "History Weighted",
                "Hot + Cold Mix",
                "Random",
            ),
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

        if (generatedChance.isNotEmpty()) {
            Text("נוצרו ${generatedChance.size} טפסי צ׳אנס", style = MaterialTheme.typography.titleSmall)
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

        Divider()
        Text("ZakenChance AI — ניתוח סטטיסטי לכיף בלבד.")
    }
}

@Composable
private fun ValidationCard(title: String, rows: List<String>) {
    Card(modifier = Modifier.fillMaxWidth()) {
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
