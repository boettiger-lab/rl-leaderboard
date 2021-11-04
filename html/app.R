leaderboard <- read.csv("../leaderboard.csv")
envs <- leaderboard["env"] %>% unique()

choices <- list()
for (i in seq_along(envs[[1]])){
  choices[[envs[[1]][i]]] <-  i
}

ui <- fluidPage(
  titlePanel("Conservation Agents Leaderboard"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("var", 
                  label = "Select the leadboard to display.",
                  choices = envs[[1]],
                  selected = envs[[1]][1])
    ),
    
    mainPanel(
      tabPanel("table", DT::dataTableOutput("table"))
    )
  )
)

server <- function(input, output){
 output$table <- DT::renderDataTable({
   DT::datatable(leaderboard %>% filter(env == input$var))
 })
}

shinyApp(ui, server)