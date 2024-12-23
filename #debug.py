try:
    from main import main
    main()
except Exception as e:
        print(e)
finally:
    input("Press Enter to exit...")